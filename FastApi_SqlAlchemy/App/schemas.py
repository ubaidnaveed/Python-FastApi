from pydantic import BaseModel


class Post(BaseModel):
    # id: int
    content: str
    description: str 

class Response(Post): 
    
    class Config:
        orm_mode = True