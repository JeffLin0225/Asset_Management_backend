import asyncio
from passlib.hash import bcrypt
from typing import Optional 
from fastapi import HTTPException

from db.mongo import get_collection
from model.user_info import UserInfo

async def verify_pin(user_id :str , input_pin :str) -> UserInfo:
    
    # 查詢條件
    user = await get_collection("user").find_one({"ID": user_id})
    user_hash = user["pwd"]

    if not user or not bcrypt.verify(input_pin, user_hash):
        raise HTTPException(status_code=401 , detail="驗證失敗")
    
    print(user["ID"] , user["name"])
    return UserInfo(ID=user["ID"] , name=user["name"])
