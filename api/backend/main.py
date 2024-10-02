import psycopg2
from fastapi.security.api_key import APIKeyHeader
from fastapi import FastAPI, Security, HTTPException, status
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Configure CORS
origins = [
    "http://192.168.1.118:5173",  # Add your frontend URL here
    "http://localhost:5173",      # Add localhost for development
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
        conn = psycopg2.connect(
            dbname="prayer_times",
            user="XXX",
            password="XXX",
            host="XXX",
            port="XXX"
        )
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


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header and validate_api_key(api_key_header):
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )


@app.get("/protected-route")
async def protected_route(api_key: str = Security(get_api_key)):
    return {"message": "You have access to this protected route"}


@app.get("/")
async def read_root():
    return {"message": "backend server is up and running..."}


@app.post("/submitHadith")
async def submit_data(request: Request, api_key: str = Security(get_api_key)):
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
        conn = psycopg2.connect(
            dbname="prayer_times",
            user="XXX",
            password="XXX",
            host="XXX",
            port="XXX"
        )
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
