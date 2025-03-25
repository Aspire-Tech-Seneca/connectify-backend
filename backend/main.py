from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from dotenv import load_dotenv
from typing import List
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Review(BaseModel):
    name: str
    comment: str

# Database connection
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("Connected to the database successfully!")
except Exception as e:
    print(f"Error connecting to the database: {e}")

@app.post("/reviews")
def add_review(review: Review):
    cur.execute("INSERT INTO reviews (name, comment) VALUES (%s, %s)", (review.name, review.comment))
    conn.commit()
    return {"message": "Review added successfully"}

@app.get("/reviews", response_model=List[Review])
def get_reviews():
    cur.execute("SELECT name, comment FROM reviews")
    rows = cur.fetchall()
    return [{"name": name, "comment": comment} for name, comment in rows]
