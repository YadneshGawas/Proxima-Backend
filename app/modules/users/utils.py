from app.extensions import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password: str, password: str) -> bool:
    """Check a plaintext password against the hashed version."""
    return bcrypt.check_password_hash(hashed_password, password)

def generate_access_token(user_id: int, expires_delta=timedelta(hours=1)) -> str:
    """Generate a JWT access token for a given user ID."""
    access_token = create_access_token(identity=user_id, expires_delta=expires_delta)
    return access_token