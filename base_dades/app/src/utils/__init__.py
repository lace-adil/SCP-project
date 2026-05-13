from sqlalchemy import create_engine
from passlib.context import CryptContext
import secrets

db_engine = create_engine("mysql+pymysql://admin:SCP!PROJECT@db/scp")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for secure storage."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_session_id() -> str:
    """Generate a secure session ID."""
    return secrets.token_urlsafe(32)

def updateDatabase():
    from os import system
    system("poetry run alembic upgrade head")