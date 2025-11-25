from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from schemas import TokenData

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_access_token(token: str, creditentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")
        if not id:
            raise creditentials_exception
        token_data = TokenData(id=id)
    except JWTError as e:
        raise creditentials_exception


# Function to verify user login
def get_curr_user(token: str = Depends(oauth2_scheme)):
    creditentials_exception = HTTPException(
        status_code=401, detail="Unathorized", headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_access_token(token, creditentials_exception)
