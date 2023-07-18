from sqlalchemy.orm import Session
from database.crud.core.crud import Crud
from database.models.models import User


class UserCrud(Crud):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)