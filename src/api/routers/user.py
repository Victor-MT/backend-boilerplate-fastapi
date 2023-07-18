from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.controllers.user_controller import UserController
from api.schemas.user_schema import UserLogginSchema, UserSchema, UserUpdateSchema
from database.database import check_db
from core.logger import logger
from database.models.models import BotLog
from datetime import datetime, timedelta

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get("/")
async def get_all_users(db: Session = Depends(check_db)):
    logger.info('Getting all users')
    return UserController(db).get_all()

@router.get("/{id}")
async def get_use_by_id(id:UUID, db: Session = Depends(check_db)):
    return UserController(db).get_by_id(id)

@router.get("/exists/{id}")
async def check_if_exists(id:UUID, db: Session = Depends(check_db)):
    return UserController(db).check_if_exists(id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchema, db: Session = Depends(check_db)):
    return UserController(db).create_user(user)

@router.put("/{id}")
async def update_user(id:str, user:UserUpdateSchema, db: Session = Depends(check_db)):
    return UserController(db).update(id, user)

@router.post("/loggin")
async def user_loggin(user: UserLogginSchema, db: Session = Depends(check_db)):
    return UserController(db).user_loggin(user)