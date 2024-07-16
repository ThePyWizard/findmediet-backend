# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class DietPlan(Base):
    __tablename__ = "diet_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(100), index=True)
    description = Column(Text)
    meals = Column(JSON)
    upvotes = Column(Integer, default=0)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
    user = relationship("User")