from fastapi import HTTPException
from fastapi.logger import logger

from cache.redis_repository import save_asset_to_redis
from db.mongo_client import asset_collection

# 查詢資料
async def find_user_asset_info( userId :str ) :
    try:

        result = await asset_collection().find_one(
            { "userId": userId },
            {"_id": 0, "asset": 1} 
        )
        return result["asset"] 
    
    except Exception as e:
        logger.exception(f"查詢使用者失敗 userId={userId}")
        return False

# 暫存邏輯
async def save_temporary_asset( userId :str , asset_data :str ) -> bool:
    try:

        await save_asset_to_redis( userId , asset_data )
        
        logger.info('儲存成功')
        return True
    
    except Exception as e:
        logger.exception(f"更新資產資料失敗 userId={userId}")
        return False
