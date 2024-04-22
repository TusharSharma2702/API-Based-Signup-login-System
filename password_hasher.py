import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()
salt = os.environ.get("salt")
salt = salt.encode('utf-8')

def hasher(password):
    hashed_password=bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password