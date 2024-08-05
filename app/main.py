from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import user , post, loginNdGetToken, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#from fastapi.params import Body
#from pydantic import BaseModel
#from sqlalchemy.orm import Session
#from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:3000", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(loginNdGetToken.router)
app.include_router(votes.router)
#@app.post("/posts2")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"message": "Successfully created posts!..."}

# my_posts = [{"title": "art of living", "conent": "content of post1", 'id':1},
#             {"title": "love life","content": "content of post2", 'id' : 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#         if p["id"] == id:
#             return(i)

