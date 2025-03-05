from jose import JWTError, jwt
from datetime import datetime, timedelta
import schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

outh2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "c9c15242bbd3fa96ee14bc766b750efffbdb39770b73a06c88b80a962e7684c9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return user_id
    
def get_current_user(token:str = Depends(outh2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception) 