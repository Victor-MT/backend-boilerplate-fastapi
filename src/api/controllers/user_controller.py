from sqlalchemy.orm import Session
from api.controllers.core.controller import Controller
from api.schemas.user_schema import UserLogginSchema, UserSchema, UserUpdateSchema
from database.crud.user_crud import UserCrud
from database.models import models


class UserController(Controller):
    def __init__(self, database: Session) -> None:
        super().__init__(database)
    
    def get_all(self):
        return UserCrud(db=self.db).get_all()
    
    def get_by_id(self, id:str):
        return UserCrud(db=self.db).get_by_id(id)
    
    def create_user(self, user:UserSchema):
        return UserCrud(db=self.db).create(models.User(**user.dict()))
    
    def update(self, id:str, user: UserUpdateSchema):
        return UserCrud(db=self.db).update(id, models.User(**user.dict()))
    
    def check_if_exists(self, id:str):
        return UserCrud(db=self.db).check_if_exists(id)
    
    def get_by_name(self, name:str):
        return self.db.query(models.User).filter(models.User.full_name.like(f"%{name}%"))
    
    def check_if_exists_by_email(self, email:str) -> models.User:
        return self.db.query(models.User).filter_by(email=email).first()

    def user_loggin(self, user:UserLogginSchema) -> models.User:
        _user = self.check_if_exists_by_email(user.email)

        return _user