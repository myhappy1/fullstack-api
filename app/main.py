from typing import List, Optional
from fastapi import FastAPI, Query
from app.recommender import item_based_recommendation,user_based_recommendation
from resolver import random_items, random_genres_items
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/") #localhost:8000/
async def all_movies():
    return {"message":"all movies"}

@app.get("/all/") #localhost:8000/
async def all_movies():
    result = random_items()
    return {"message":result}


@app.get("/genres/{genre}")
async def genre_movies(genre: str):
    result = random_genres_items(genre)
    return {"result": result}

@app.get("/user-based/")
async def user_based(params:Optional[List[str]] = Query(None)):
    input_ratings_dict = dict(
        (int(x.split(":")[0]), float(x.split(":")[1]))for x in params)
    
    result = user_based_recommendation(input_ratings_dict)
    return {"result":result}

@app.get("/item-based/{item_id}")
async def user_based(item_id: str):
    result = item_based_recommendation(item_id)
    return {"message": f"item based:{item_id}"}