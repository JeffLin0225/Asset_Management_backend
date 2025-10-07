from fastapi.logger import logger
from datetime import datetime
from db.mongo_client import asset_collection ,analyze_collection

# 查詢資料
async def select_user_asset_info( userId :str ) -> bool:
    try:

        result = await asset_collection().find_one(
            { "userId": userId },
            {"_id": 0, "asset": 1} 
        )
        return result["asset"] 
    
    except Exception as e:
        logger.exception(f"查詢使用者失敗 userId={userId}")
        return False

# 儲存邏輯
async def save_asset( userId :str , asset_data :str ) -> bool:
    try:

        # 存入 mongoDB
        result = await asset_collection().update_one(
                    { "userId" : userId },
                    { "$set" : asset_data },
                    upsert=False
                )
        if result.modified_count == 0:
            logger.error("沒有使用者資訊，無法儲存")
            return False
        
        logger.info('儲存成功')
        return True
    
    except Exception as e:
        logger.exception(f"更新資產資料失敗 userId={userId}")
        return False

# 儲存邏輯
async def save_analyze( userId :str , asset_data :str ) -> bool:
    try:

        # 存入 mongoDB
        result = await analyze_collection().insert_one({
                    "userId" : userId,
                    "asset" : asset_data,
                    "date" : datetime.now(datetime.day)
                })

        if not result.inserted_id:
            logger.exception("新增分析失敗，沒有 inserted_id")
            return False
        
        logger.info('新增分析成功:'+result)
        return True
    
    except Exception as e:
        logger.exception(f"新增資產分析資料失敗 userId={userId}")
        return False
