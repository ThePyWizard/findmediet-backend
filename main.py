from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine, Base
from models import User, DietPlan
from schemas import User as UserSchema, DietPlan as DietPlanSchema, DietPlanCreate
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specify which origins are allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/diet_plans/", response_model=List[DietPlanSchema])
def read_diet_plans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    diet_plans = db.query(DietPlan).offset(skip).limit(limit).all()
    return diet_plans

@app.get("/diet_plans/{diet_plan_id}", response_model=DietPlanSchema)
def read_diet_plan(diet_plan_id: int, db: Session = Depends(get_db)):
    diet_plan = db.query(DietPlan).filter(DietPlan.id == diet_plan_id).first()
    if diet_plan is None:
        raise HTTPException(status_code=404, detail="Diet Plan not found")
    return diet_plan

@app.post("/diet_plans/", response_model=DietPlanSchema)
def create_diet_plan(diet_plan: DietPlanCreate, db: Session = Depends(get_db)):
    db_diet_plan = DietPlan(**diet_plan.dict())
    db.add(db_diet_plan)
    db.commit()
    db.refresh(db_diet_plan)
    return db_diet_plan
