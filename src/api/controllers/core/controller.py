from sqlalchemy.orm import Session
from api.schemas.core.schema import Schema

class Controller:
    db: Session

    def __init__(self, db: Session) -> None:
        self.db = db

    def map_to_model(self, schema, model):
        return Schema.to_model_dict(schema, model)
