# schemas.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class DietPlanBase(BaseModel):
    title: str
    description: str
    meals: Any
    upvotes: int

class DietPlanCreate(DietPlanBase):
    pass

class DietPlan(DietPlanBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True