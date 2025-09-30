from fastapi import HTTPException
import os 
from dotenv import load_dotenv
from fastapi.logger import logger

from cache.redis_repository import save_asset_to_redis
from db.mongo import asset_collection

# async def save_asset_data(userId, asset_data = ''):
    
    # 1.查詢是否有使用者資料
    # has_user_info :bool = await find_user_asset_info()
    # if not has_user_info:
    #     raise HTTPException(status_code=404 , detail="沒有使用者資訊，無法儲存")
    
    # upsert_user_asset_info(userId , asset_data = '')
    

    # 暫存邏輯
async def temporary_asset_save( userId :str , asset_data :str ) -> bool:
    try:

        # # 存入 mongoDB
        # result = await asset_collection().update_one(
        #             { "userId" : userId },
        #             { "$set" : asset_data },
        #             upsert=False
        #         )
        # if result.modified_count == 0:
        #     logger.error("沒有使用者資訊，無法儲存")
        #     return False
        await save_asset_to_redis( userId , asset_data )
        
        logger.info('儲存成功')
        return True
    
    except Exception as e:
        logger.exception(f"更新資產資料失敗 userId={userId}")
        return False


# async def find_user_asset_info( userId :str ) -> bool:
#     try:

#         result = await asset_collection().find_one(
#             { "userId": userId }
#         )
#         return result is not None
    
#     except Exception as e:
#         logger.exception(f"查詢使用者失敗 userId={userId}")
#         return False