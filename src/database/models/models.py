from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, Column, DateTime, String
from ..database import Database
import datetime
import uuid

class User(Database):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime)
