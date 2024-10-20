import datetime
import os
from typing import Annotated
import psycopg2
from config import load_config
from fastapi.security.api_key import APIKeyHeader
from fastapi import FastAPI, Security, HTTPException, status
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket, WebSocketDisconnect


from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse
import json


# todo: make error handeling better
def check_prerequisites():
    try:
        if not os.path.isfile("database.ini"):
            raise FileNotFoundError(f"The file database.ini does not exist.")
    except Exception as e:
        print(f"Error checking prerequisites: {e}")
        return False


check_prerequisites()

app = FastAPI()
connections = []

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


API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Function to validate API key from database


def validate_api_key(api_key: str) -> bool:
    try:
        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()

        # Query to check if the key exists and is active
        cursor.execute(
            "SELECT COUNT(*) FROM api_keys WHERE key = %s AND active = TRUE",
            (api_key,)
        )
        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return result > 0

    except Exception as e:
        print(f"Error validating API key: {e}")
        return False


async def get_api_key_http(api_key_header: str = Depends(api_key_header)):
    print(f"API Key Header: {api_key_header}")
    if api_key_header and validate_api_key(api_key_header):
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )


@app.get("/protected-route")
async def protected_route(api_key: str = Depends(get_api_key_http)):
    return {"message": "You have access to this protected route"}


@app.get("/")
async def read_root():
    return {"message": "backend server is up and running..."}


@app.post("/submitHadith")
async def submit_data(request: Request, api_key: str = Depends(get_api_key_http)):
    try:
        data = await request.json()

        deutsch = data.get("deutsch")
        turkisch = data.get("turkisch")
        quelle = data.get("quelle")

        if not all([deutsch, turkisch, quelle]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing data in request"
            )

        print(f"Data received: {deutsch}, {turkisch}, {quelle}")

        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute(
            "INSERT INTO hadiths (deutsch, turkisch, quelle) VALUES (%s, %s, %s)",
            (deutsch, turkisch, quelle)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Data saved successfully"}
    except Exception as e:
        print(f"Error saving data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving data"
        )


@app.get("/randomHadith")
async def get_random_hadith(api_key: str = Depends(get_api_key_http)):
    try:
        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()

        # Query to get a random hadith
        cursor.execute(
            "SELECT deutsch, turkisch, quelle FROM hadiths ORDER BY RANDOM() LIMIT 1"
        )
        hadith = cursor.fetchone()

        cursor.close()
        conn.close()

        if hadith:
            return {"deutsch": hadith[0], "turkisch": hadith[1], "quelle": hadith[2]}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hadith found"
            )
    except Exception as e:
        print(f"Error getting random hadith: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting random hadith"
        )

@app.get("/getAllHadith")
async def get_all_hadiths(api_key: str = Depends(get_api_key_http)):
    try:
        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()

        # Query to get all hadiths
        cursor.execute("SELECT deutsch, turkisch, quelle FROM hadiths")
        hadiths = cursor.fetchall()

        cursor.close()
        conn.close()

        return {"hadiths": [{"deutsch": h[0], "turkisch": h[1], "quelle": h[2]} for h in hadiths]}
    except Exception as e:
        print(f"Error getting all hadiths: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting all hadiths"
        )

async def get_api_key_ws(token: str = None):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token


@app.get("/announcements")
async def get_announcements(api_key: str = Depends(get_api_key_http)):
    try:
        # Connect to PostgreSQL
        config = load_config()

        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL database")

        cursor = conn.cursor()
        date = datetime.datetime.now()

        # Query to get announcements
        cursor.execute(
            "SELECT * FROM announcements WHERE api_key_id = (SELECT id FROM api_keys WHERE key = %s) AND end_date > %s AND active = TRUE",
            (api_key, date)
        )
        announcements = cursor.fetchall()

        cursor.close()
        conn.close()

        return {"announcements": announcements}
    except Exception as e:
        print(f"Error getting announcements: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting announcements"
        )


class MyWebsocket:
    def __init__(self, websocket: WebSocket, token: str):
        self.websocket = websocket
        self.token = token


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
                    await websocket.send_text(f"Announcement: {json_data}")
                    # TODO: save announcment in database
                    # get apikey id and save it with the announcments in the database

                    try:
                        # Connect to PostgreSQL
                        config = load_config()

                        conn = psycopg2.connect(**config)
                        print("Connected to PostgreSQL database")

                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT id FROM api_keys WHERE key = %s AND active = TRUE",
                            (token,)
                        )
                        api_key_id = cursor.fetchone()[0]

                        print(json_data.get("start_date"))
                        cursor.execute(
                            "INSERT INTO announcements (message_german, message_turkish, start_date, end_date, api_key_id) VALUES (%s, %s, %s, %s, %s)",
                            (
                                json_data.get("message_german"),
                                json_data.get("message_turkish"),
                                json_data.get("start_date"),
                                json_data.get("end_date") if json_data.get(
                                    "end_date") else datetime.datetime.now() + datetime.timedelta(days=365*10),
                                api_key_id
                            )
                        )
                        conn.commit()

                        cursor.close()
                        conn.close()

                        for connection in connections:
                            if connection.websocket != websocket and connection.token == token:
                                await connection.websocket.send_text(f"{data}")
                    except Exception as e:
                        print(f"Error saving announcement: {e}")
                        await websocket.send_text(f"Error saving announcement: {e}")
                else:
                    await websocket.send_text(f"Invalid type: {json_data}")
                    return
            except json.JSONDecodeError as e:
                await websocket.send_text(f"Invalid JSON data: {e}")
                return

    except WebSocketDisconnect:
        print("Client disconnected")
        for connection in connections:
            if connection.websocket == websocket:
                connections.remove(connection)
                break
        print("Client disconnected")
