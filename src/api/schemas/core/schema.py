from typing import Type, TypeVar
from pydantic import BaseModel, validator 

T = TypeVar('T')
class Schema(BaseModel):
    
    @validator('*', pre=True)
    def striping_strings(cls, v, field):
        if issubclass(field.type_, str) and bool(v):
            try:
                return str(v).strip()
            except Exception as e:
                print(e)
        return v
    
    @staticmethod
    def to_model_dict(schema, model):
        common_fields = set(model.__table__.columns.keys()) & set(schema.dict().keys())
        return {field: schema.dict()[field] for field in common_fields}

    @classmethod
    def parse_obj_selective(cls: Type[T], data: dict) -> T:
        common_fields = set(cls.__annotations__.keys()) & set(data.keys())

        atributos = {k: v for k, v in data.items() if k in common_fields}

        return cls(**atributos)