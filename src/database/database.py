from fastapi import HTTPException, Request, status
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.DB_CONTAINER}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    except Exception as e:
        raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY, 
                    detail="Database out of work:" + str(e)
                )
    finally:
        db.close()

async def check_db(request: Request):
    if not hasattr(request.state, "db") or request.state.db is None:
        raise HTTPException(
                            status_code=status.HTTP_502_BAD_GATEWAY, 
                            detail="Database session not available"
                            )
    
    return request.state.db

class Database(Base):
    __abstract__ = True

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
    
    def save(self, session: Session):
        try:
            if self.id is None:
                session.add(self)
            else:
                session.merge(self)

            session.flush()
            session.refresh(self)

        except IntegrityError as e:
            session.rollback()
            raise e
        except SQLAlchemyError as e:
            session.rollback()
            raise e
    
    def save_and_commit(self, session: Session):
        self.save(session)
        session.commit()