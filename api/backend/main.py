import datetime
import os
import jwt
import psycopg2
from pydantic import BaseModel
from config import load_config
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketException,
    WebSocketState,
    status,
    Request,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
import json
from jwt import ExpiredSignatureError, InvalidTokenError, InvalidSignatureError
import requests
from dotenv import load_dotenv

# todo: make error handeling better


def check_prerequisites():
    try:
        if not os.path.isfile("database.ini"):
            logging.error("The file database.ini does not exist.")
            raise FileNotFoundError(f"The file database.ini does not exist.")
    except Exception as e:
        logging.error(f"Error checking prerequisites: {e}")
        return False


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S', filename='logs.log'
)

logger = logging.getLogger(__name__)


logger.info("App started")

check_prerequisites()

app = FastAPI()
connections = []
listen_connections = []

# Configure CORS
origins = [
    # "http://192.168.1.118:5173",
    # "http://localhost:5173",
    # "https://prayer-time.berkkan.de/",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_KEY_NAME = "X-TOKEN"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Function to validate API key from database


def validate_jwt_token(jwt_token: str) -> bool:
    # Fetch the JWKS from Authentik
    jwks = get_jwks()

    # Decode the JWT header to get the 'kid' (Key ID)
    unverified_header = jwt.get_unverified_header(jwt_token)
    kid = unverified_header['kid']

    # Get the public key based on 'kid' from JWKS
    public_key = get_public_key(jwks, kid)

    # Verify the JWT with the public key
    # print("\n--- Verifying JWT with the public key ---")
    return verify_jwt(jwt_token, public_key)


# Endpoint for fetching the JWKS from Authentik
JWKS_URL = "https://auth.berkkan.de/application/o/hadith-api/jwks/"


def get_jwks():
    """Fetch the JWKS from the Authentik endpoint."""
    response = requests.get(JWKS_URL)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to fetch JWKS: {
            response.status_code}, {response.json()}")
        raise Exception(f"Failed to fetch JWKS: {response.status_code}")


def get_public_key(jwks, kid):
    """Extract the public key corresponding to the JWT's 'kid'."""
    for key in jwks['keys']:
        if key['kid'] == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    logger.error(f"Public key not found for kid: {kid}")
    raise Exception(f"Public key not found for kid: {kid}")


def verify_jwt(token, public_key):
    """Decode and verify the JWT using the public key."""
    try:
        unverified_token = decode_jwt_unverified(token)
        aud = unverified_token.get("aud")
        verified_token = jwt.decode(token, public_key, algorithms=[
                                    "RS256"], audience=aud, options={"verify_exp": True})
        # print("Verified Token Payload:", verified_token)
        return True
    except ExpiredSignatureError:
        logger.error("Token has expired")
        return False
    except InvalidSignatureError:
        logger.error("Invalid signature")
        return False
    except InvalidTokenError as e:
        logger.error(f"Invalid token {e}")
        return False


def decode_jwt_unverified(token):
    return jwt.decode(token, options={"verify_signature": False})


def decode_jwt(token):
    # Fetch the JWKS from Authentik
    jwks = get_jwks()

    # Decode the JWT header to get the 'kid' (Key ID)
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header['kid']

    # Get the public key based on 'kid' from JWKS
    public_key = get_public_key(jwks, kid)

    unverified_token = decode_jwt_unverified(token)
    aud = unverified_token.get("aud")

    # Verify the JWT with the public key
    return jwt.decode(token, public_key, algorithms=["RS256"], audience=aud, options={"verify_exp": True})


async def get_api_key_http(api_key_header: str = Depends(api_key_header)):
    if api_key_header and validate_jwt_token(api_key_header):
        return api_key_header
    else:
        logger.error("Invalid or missing API Key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )


def getMosque(jwt):
    decode = decode_jwt(jwt)
    group = decode.get("groups")
    for g in group:
        if "mosque" in g:
            return g
    logger.warning("No mosque group found in token")
    return None


@app.get("/protected-route")
async def protected_route(api_key: str = Depends(get_api_key_http)):
    return {"message": "You have access to this protected route"}


@app.get("/")
async def read_root():
    return {"message": "backend server is up and running..."}


class TokenRefreshRequest(BaseModel):
    refresh_token: str


@app.post("/refresh-token")
async def refresh_token(request: TokenRefreshRequest):
    logger.info(f"Refreshing token: {request.refresh_token}")
    try:
        load_dotenv()

        response = requests.post("https://auth.berkkan.de/application/o/token/", data={
            "grant_type": "refresh_token",
            "refresh_token": request.refresh_token,
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
        })

        if response.status_code != 200:
            logger.error(f"Failed to refresh token error: {response.json()}")
            raise HTTPException(status_code=response.status_code,
                                detail=f"Failed to refresh token error: {response.json()}")
        logger.info(f"Token refreshed: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to refresh token error: {e}, {response.json()}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/checkUserLogin")
async def check_user_login(api_key: str = Depends(get_api_key_http)):
    decode = decode_jwt(api_key)
    group = decode.get("groups")
    if ("first-login" in group):
        try:
            load_dotenv()

            username = decode.get("preferred_username")
            user_response = requests.get(
                f"https://auth.berkkan.de/api/v3/core/users/?username={
                    username}",
                headers={"accept": "application/json",
                         "authorization": f"Bearer {os.getenv('API_KEY')}"},
            )

            if user_response.status_code != 200:
                raise HTTPException(
                    status_code=user_response.status_code, detail="Failed to fetch user details")

            user_data = user_response.json()
            user_pk = user_data["results"][0]['pk']

            group_uuid = os.getenv("FIRST_LOGIN_GROUP_UUID")
            remove_user_response = requests.post(
                f"https://auth.berkkan.de/api/v3/core/groups/{
                    group_uuid}/remove_user/",
                headers={"accept": "application/json",
                         "content-type": "application/json",
                         "authorization": f"Bearer {os.getenv('API_KEY')}"},
                json={"pk": user_pk}
            )

            if remove_user_response.content:
                print(remove_user_response.json())
            else:
                print("No content in response")

        except Exception as e:
            logger.error(f"Error removing user from group: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to remove user from group")

    return {"message": "User is logged in"}


@app.post("/submitHadith")
async def submit_data(request: Request, api_key: str = Depends(get_api_key_http)):
    try:
        data = await request.json()

        deutsch = data.get("deutsch")
        turkisch = data.get("turkisch")
        quelle = data.get("quelle")
        mosque = getMosque(api_key)

        if not all([deutsch, turkisch, quelle]):
            logger.warning("Missing data in request")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing data in request"
            )

        print(f"Data received: {deutsch}, {turkisch}, {quelle}, {mosque}")

        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute(
            "INSERT INTO hadiths (deutsch, turkisch, quelle, mosque) VALUES (%s, %s, %s, %s)",
            (deutsch, turkisch, quelle, mosque)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Data saved successfully"}
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving data"
        )


@app.post("/randomHadith")
async def get_random_hadith(request: Request):
    try:
        data = await request.json()
        mosque = data.get("mosque")

        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()

        # Query to get a random hadith
        cursor.execute(
            "SELECT deutsch, turkisch, quelle FROM hadiths WHERE mosque = %s ORDER BY RANDOM() LIMIT 1",
            (mosque,)
        )
        hadith = cursor.fetchone()

        cursor.close()
        conn.close()

        if hadith:
            return {"deutsch": hadith[0], "turkisch": hadith[1], "quelle": hadith[2]}
        else:
            logger.warning("No hadith found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hadith found"
            )
    except Exception as e:
        logger.error(f"Error getting random hadith: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting random hadith"
        )


@app.get("/getAllHadith")
async def get_all_hadiths(api_key: str = Depends(get_api_key_http)):
    try:
        mosque = getMosque(api_key)

        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()

        # Query to get all hadiths
        cursor.execute(
            "SELECT deutsch, turkisch, quelle FROM hadiths WHERE mosque = %s",
            (mosque,)
        )
        hadiths = cursor.fetchall()

        cursor.close()
        conn.close()

        return {"hadiths": [{"deutsch": h[0], "turkisch": h[1], "quelle": h[2]} for h in hadiths]}
    except Exception as e:
        logger.error(f"Error getting all hadiths: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting all hadiths"
        )


async def get_api_key_ws(token: str = None):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    if validate_jwt_token(token):
        return token


@app.post("/announcements")
async def get_announcements(request: Request):
    try:
        data = await request.json()
        mosque = data.get("mosque")

        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()
        date = datetime.datetime.now()

        # Query to get announcements
        cursor.execute(
            "SELECT * FROM announcements WHERE mosque = %s AND end_date > %s AND active = TRUE",
            (mosque, date)
        )
        announcements = cursor.fetchall()

        cursor.close()
        conn.close()

        return {"announcements": announcements}
    except Exception as e:
        logger.error(f"Error getting announcements: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting announcements"
        )


class MyWebsocket:
    def __init__(self, websocket: WebSocket, token: str):
        self.websocket = websocket
        self.token = token


class ListenWebsocket:
    def __init__(self, websocket: WebSocket, mosque: str):
        self.websocket = websocket
        self.mosque = mosque


@app.websocket("/ws-listen")
async def websocket_listen_endpoint(websocket: WebSocket, mosque: str):
    await websocket.accept()
    print("Client connected to listen")
    listenWebsocket = ListenWebsocket(websocket=websocket, mosque=mosque)
    listen_connections.append(listenWebsocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        listen_connections.remove(listenWebsocket)
        logger.info(f"Length of the listen_connection): {
                    len(listen_connections)}")
        logger.info("Client disconnected from listen")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_api_key_ws)):
    await websocket.accept()
    print("Client connected")
    myWebsocket = MyWebsocket(websocket=websocket, token=token)
    connections.append(myWebsocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                json_data = json.loads(data)
                if (json_data.get("type") == "announcement"):
                    await websocket.send_text(f"You send this Announcement: {json_data}")

                    try:
                        mosque = getMosque(token)

                        # Connect to PostgreSQL
                        config = load_config()

                        conn = psycopg2.connect(**config)
                        print("Connected to PostgreSQL database")

                        cursor = conn.cursor()

                        print(json_data.get("start_date"))
                        cursor.execute(
                            "INSERT INTO announcements (message_german, message_turkish, start_date, end_date, mosque) VALUES (%s, %s, %s, %s, %s)",
                            (
                                json_data.get("message_german"),
                                json_data.get("message_turkish"),
                                json_data.get("start_date"),
                                json_data.get("end_date") if json_data.get(
                                    "end_date") else datetime.datetime.now() + datetime.timedelta(days=365*10),
                                mosque
                            )
                        )
                        conn.commit()

                        cursor.close()
                        conn.close()
                    except Exception as e:
                        logger.error(f"Error saving announcement to DB: {e}")

                    for connection in listen_connections:
                        if connection.mosque == mosque:
                            if connection.websocket.application_state == WebSocketState.CONNECTED:
                                logger.info(
                                    f"Sending announcement to mosque: {mosque}")
                                await connection.websocket.send_text(f"{data}")
                                logger.info("Done")
                            else:
                                logger.warning(f"Connection to mosque {
                                               mosque} is not open")
                                logger.info(f"Length of the listen_connection): {
                                            len(listen_connections)}")

                else:
                    logger.error(f"Invalid type: {json_data}")
                    await websocket.send_text(f"Invalid type: {json_data}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON data: {e}")
                await websocket.send_text(f"Invalid JSON data: {e}")
            except Exception as e:
                logger.error(f"Error: {e}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
        connections.remove(myWebsocket)
    except Exception as e:
        logger.error(f"Error: {e}")
