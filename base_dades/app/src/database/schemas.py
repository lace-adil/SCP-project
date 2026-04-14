from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class SCPSubject(BaseModel):
    id: int = -1
    object_class: str = None
    containment_procedures: str = None
    description: str = None
    

class DB_SCPSubject(Base):
    __tablename__ = "scp_subjects"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    object_class = sa.Column(sa.VARCHAR(15))
    containment_procedures = sa.Column(sa.VARCHAR(1024))
    description = sa.Column(sa.VARCHAR(4096))