from sqlalchemy import text, Column, TIMESTAMP, Integer, String
from sqlalchemy.sql.expression import null

from .database import Base

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    content=Column(String,nullable=False)
    description = Column(String,nullable=False)
                        
