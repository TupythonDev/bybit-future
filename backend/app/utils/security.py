from passlib.context import CryptContext
from cryptography.fernet import Fernet
from app.core.config import settings

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return PWD_CONTEXT.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def encrypt_secret(secret:str) -> str:
    return Fernet(settings.fernet_key).encrypt(secret.encode()).decode()

def decrypt_secret(secret:str) -> str:
    return Fernet(settings.fernet_key).decrypt(secret.encode()).decode()
