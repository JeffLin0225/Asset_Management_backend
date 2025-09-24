from passlib.hash import bcrypt
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta ,timezone
import os 
from dotenv import load_dotenv
from fastapi.logger import logger

from db.mongo import get_collection
from model.user_info import UserInfo
from dto.login_dto import LoginResponse

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("EXPIRE_MINUTES"))

async def verify_pin(user_id :str , input_pin :str) -> str:
    
    # 查詢條件
    user = await get_collection("user").find_one({"ID": user_id})

    if not user:
        logger.error("[驗證Fail] 沒有這個使用者 使用者輸入的 ID： "+user_id+" , 使用者輸入的PIN："+input_pin)
        raise HTTPException(status_code=401 , detail="驗證失敗")
    
    if not bcrypt.verify(input_pin, user["pwd"]):
        logger.error("[驗證Fail] 使用者密碼錯誤 ID="+user["ID"]+" , 你的輸入："+input_pin)
        raise HTTPException(status_code=401 , detail="驗證失敗")
    
    jwt_token :str= await create_access_token(UserInfo(ID=user["ID"] , name=user["name"]))
    logger.info("ID= "+user["ID"] + " , name= "+user["name"] + " , JWT= " + jwt_token)

    return LoginResponse(
            ID = user["ID"], 
            name =  user["name"],  
            access_token = jwt_token
        )

async def create_access_token(user_data :UserInfo) -> str:
    to_encode = user_data.model_dump()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)

