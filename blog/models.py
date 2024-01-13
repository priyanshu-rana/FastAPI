from sqlalchemy import Boolean, Column, Integer, String
from .database import Base


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    is_published = Column(Boolean)
