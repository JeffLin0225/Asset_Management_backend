from fastapi import HTTPException
import os 
from dotenv import load_dotenv
from fastapi.logger import logger

from db.mongo import asset_collection

async def save_asset_data():
    
    # 1.查詢是否有使用者資料
    has_user_info = await find_user_asset_info()
    if has_user_info:




async def find_user_asset_info( userId :str ) -> bool:

    await asset_collection().find_one(
        { "userId": userId }
    )

async def upsert_user_asset_info( userId :str , asset_data :str ) -> bool:

    await asset_collection().update_one(
        { "userId" : userId },
        { "$set" : asset_data },
        upsert=False
    )