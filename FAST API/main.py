# python -m uvicorn main:app --reload
# http://127.0.0.1:8000/

from uuid import uuid4
import json
from typing import Optional, Literal
from fastapi import FastAPI, HTTPException
import random
import os
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# Movie model
class Movie(BaseModel):
    name: str
    price: float
    genre: Literal["Action", "Romance", "Comedy"]
    id: Optional[str] = uuid4().hex

MOVIES_FILE = "movie.json"
MOVIE_DATABASE = [
]

if os.path.exists(MOVIES_FILE):
    with open(MOVIES_FILE, "r") as f:
        MOVIE_DATABASE = json.load(f)

# /
@app.get("/")
async def home():
    return {"Message": "Welcome to my online Movie store!"}

# /list-movies
@app.get("/list-movies")
async def list_movies():
    return {"Movies": MOVIE_DATABASE}

# /movie-by-index/{index} /movie-by-index/0
@app.get("/movie-by-index/{index}")
async def movie_by_id(index: int):
    if index < 0 or index >= len(MOVIE_DATABASE):
        raise HTTPException(404, f"Index {index} is out of range {len(MOVIE_DATABASE)}.")
    else:
        return {"Movie": MOVIE_DATABASE[index]}
    
# /get-random-movie
@app.get("/get-random-movie")
async def get_random_movie():
    return random.choice(MOVIE_DATABASE)

# /add-movie
@app.post("/add-movie")
async def add_movie(movie: Movie):
    movie.id = uuid4().hex
    json_movie = jsonable_encoder(movie)
    MOVIE_DATABASE.append(json_movie)
    with open(MOVIES_FILE, "w") as f:
        json.dump(MOVIE_DATABASE, f)
    return{"Message": f"{movie} has been added to our database!", "Movie ID": movie.id}


# /get-movie?id=...
@app.get("/get-movie")
async def get_movie(movie_id: str):
    for movie in MOVIE_DATABASE:
        if movie["id"] == movie_id:
            return movie
        
    raise HTTPException(404, f"Movie not found {movie_id}.")

