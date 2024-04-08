from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

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
# post_array= [{"id":1, "content":"Cryptography" , "description":"Billionaire"},{"id":2, "content":"Banking" , "description":"Billionaire"}]
 
# def check(id):
#     for a in post_array:
#         if a['id']==id: 
#             return a

# def Index(id):
#     for i,a in enumerate(post_array):
#         if a['id']==id: 
#             return i


class Post(BaseModel):
    # id: int
    content: str
    description: str 

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def post():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()              
    return{"Data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # post_array.append(post.model_dump())
    cursor.execute("""INSERT INTO posts(content,description) VALUES(%s,%s) RETURNING * """,(post.content,post.description))
    post=cursor.fetchone()
    conn.commit()
    return {"Data":post}

@app.get("/posts/{id}")
def post(id:int, response:Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
    post=cursor.fetchone()
    # found= check(id)
    if not post:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": f"{description} Not Found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} Not Found")
    
    return{"Data":post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""Delete from posts where id=%s RETURNING * """,(str(id)))
    deletedPost=cursor.fetchone()
    conn.commit()
    # found=Index(id)
    if deletedPost==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} Not Found")
    # post_array.pop(found)
    return{Response(status_code=status.HTTP_204_NO_CONTENT)}    

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""Update posts SET content=%s,description=%s where id=%s RETURNING * """,(post.content,post.description,str(id)))
    updatedPost=cursor.fetchone()
    conn.commit()
    # found=Index(id)
    if updatedPost==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} Not Found")
    # post_array[found]=post.model_dump()
    return{"Data":updatedPost}

