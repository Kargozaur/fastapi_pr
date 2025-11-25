# function to hash password
import hashlib

import bcrypt


# functio to create hashed password
def hash_password(password: str):
    sha = hashlib.sha256(password.encode()).digest()
    return bcrypt.hashpw(sha, bcrypt.gensalt()).decode()


# function to verify password
def verify_password(password: str, hashed: str):
    sha = hashlib.sha256(password.encode()).digest()
    return bcrypt.checkpw(sha, hashed.encode())
