from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
# from model.user_info import UserInfo

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

async def verify_token(token :str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        expire = payload.get("exp")
        if expire is None or datetime.fromtimestamp(expire, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token 已過期",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # return UserInfo(**payload)
        return None #不回傳
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認證無效",
            headers={"WWW-Authenticate": "Bearer"},
        )