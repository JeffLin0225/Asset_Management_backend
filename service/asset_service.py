from fastapi import HTTPException
from fastapi.logger import logger

from cache.redis_repository import save_asset_to_redis
from db.mongo_repository import select_user_asset_info

# 查詢資料
async def find_user_asset_info( userId :str )  -> bool:

        return await select_user_asset_info(userId)

# 暫存邏輯
async def save_temporary_asset( userId :str , asset_data :str ) -> bool:
    try:

        await save_asset_to_redis( userId , asset_data )
        
        return True
    
    except Exception as e:
        logger.exception(f"更新資產資料失敗 userId={userId}")
        return False
