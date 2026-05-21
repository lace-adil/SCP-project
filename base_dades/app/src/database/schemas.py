from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
import sqlalchemy as sa

Base = declarative_base()

class SCPSubject(BaseModel):
    id: int = -1
    object_class: Optional[str] = None
    containment_procedures: Optional[str] = None
    description: Optional[str] = None
    chamber_id: Optional[int] = None
    assigned_researcher_id: Optional[int] = None

class User(BaseModel):
    id: int = -1
    username: str
    password: str = None

class UserLogin(BaseModel):
    username: str
    password: str
    

class DB_SCPSubject(Base):
    __tablename__ = "scp_subjects"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    object_class = sa.Column(sa.VARCHAR(15))
    containment_procedures = sa.Column(sa.VARCHAR(1024))
    description = sa.Column(sa.VARCHAR(4096))
    chamber_id = sa.Column(sa.Integer)
    assigned_researcher_id = sa.Column(sa.Integer)

class DB_User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.VARCHAR(45), nullable=False, unique=True)
    password = sa.Column(sa.VARCHAR(255), nullable=False)