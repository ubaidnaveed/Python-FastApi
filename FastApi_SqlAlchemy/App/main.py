from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import List
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Enter Password',cursor_factory=RealDictCursor)
        cursor= conn.cursor()
        print("Connected to database")
        break
    except Exception as error:
        print("Failed to connect to database. Kindky check if u have entered the right user and password.")
        print(error)
        time.sleep(2)

 

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts",response_model=List[schemas.Response])
def post(db:Session= Depends(get_db)):
    posts=db.query(models.Posts).all()            
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.Response)
def create_post(post: schemas.Post,db:Session= Depends(get_db)):
    # post= models.Post(content= post.content, description=post.description)
    newPost=models.Posts(**post.model_dump())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost


@app.get("/posts/{id}",response_model=schemas.Response)
def post(id:int, db:Session=Depends(get_db)):
    post=db.query(models.Posts).filter(models.Posts.id==id).first()
    if not post:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": f"{description} Not Found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} Not Found")    
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    deletedPost=db.query(models.Posts).filter(models.Posts.id==id)
    if deletedPost.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} Not Found")
    deletedPost.delete(synchronize_session=False)
    db.commit()
    return{Response(status_code=status.HTTP_204_NO_CONTENT)}    


@app.put("/posts/{id}",response_model=schemas.Response)
def update_post(id:int,post:schemas.Post,db:Session=Depends(get_db)):
    Post=db.query(models.Posts).filter(id==id)
    Post.update(post.model_dump(),synchronize_session=False)
    if Post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} Not Found")
    db.commit()
    return Post.first()

