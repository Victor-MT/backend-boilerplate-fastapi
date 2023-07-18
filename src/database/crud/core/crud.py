from typing import TypeVar, Generic, List,Union
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound
from sqlalchemy.orm import Session
from typing import Union

T = TypeVar('T')

class Crud(Generic[T]):
    db: Session
    model: T.__class__

    def __init__(self, db: Session, model: T.__class__) -> None:
        self.db = db
        self.model = model

    def create(self, obj: T) -> T:
        #return
        try:
            self.db.add(obj)
            self.db.flush()
            self.db.refresh(obj)
            return obj
        except IntegrityError as e:
            self.db.rollback()
            raise e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e
        
    def create_range(self, obj: List[T]) -> List[T]:
        try:
            self.db.add_all(obj)
            self.db.flush()
            return obj
        
        except IntegrityError as e:
            self.db.rollback()
            raise e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update(self, id: str, data: T) -> T:
        #return
        obj = self.get_by_id(id)
        
        for field, value in data.as_dict().items():
            if not value is None:
                if value == 'None': value = None
                setattr(obj, field, value)      

        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: str) -> T:
        obj = self.get_by_id(id)
        self.db.delete(obj)
        self.db.flush()
        return obj
    
    def get_by_id(self, id: str) -> T:
        obj = self.db.query(self.model).get(id)
        if obj is None:
            raise NoResultFound()
        return obj

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def check_if_exists(self, id: str) -> Union[str, None]:
        """
        Verifica se um objeto com o ID fornecido já existe no banco de dados.
        Retorna o ID do objeto se existir ou None caso contrário.
        """
        obj = self.db.query(self.model).filter_by(id=id).first()
        if obj is None:
            return None
        else:
            return obj.id
