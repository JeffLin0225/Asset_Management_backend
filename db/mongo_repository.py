from fastapi.logger import logger
from typing import List 

from model.snapshot import Snapshot 
from db.mongo_client import asset_collection ,analyze_collection , user_collection

# 查詢資產資料
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

# 儲存資產邏輯
async def save_asset( userId :str , asset_data :str ) -> bool:
    try:

        # 存入 mongoDB
        result = await asset_collection().update_one(
                    { "userId" : userId },
                    { "$set" :  { "asset": asset_data } },
                    upsert=False
                )
        if result.matched_count == 0:
            logger.error("沒有使用者資訊，無法儲存")
            return False

        if result.modified_count == 0:
            logger.info("資料相同，沒有更新任何欄位")
            return True   # 這裡可以視為成功，只是沒有變動
        
        logger.info('儲存成功')
        return True
    
    except Exception as e:
        logger.exception(f"更新資產資料失敗 userId={userId}")
        return False


# 查詢分析資料
async def select_user_analyze_info( userId :str ) -> list[dict]:
    try:

        result = await analyze_collection().find(
            { "userId": userId }
        ).to_list(length=None)
        return result
    
    except Exception as e:
        logger.exception(f"查詢使用者失敗 userId={userId}")
        return False

# 儲存分析邏輯
async def save_analyze(snapshot: Snapshot) -> bool:
    try:
        # upsert：存在就更新，不存在就新增
        await analyze_collection().update_one(
            {"userId": snapshot.userId, "date": snapshot.date},
            {"$set": snapshot.model_dump()},
            upsert=True
        )
        logger.info(f"✅ Snapshot 已存入/更新 userId={snapshot.userId}, date={snapshot.date}")
        return True

    except Exception as e:
        logger.exception(f"❌ 儲存 Snapshot 失敗 userId={snapshot.userId}, date={snapshot.date}")
        raise

# 查詢所有使用者
async def select_all_user_id() -> List[str]:
    try:

        cursor = user_collection().find({}, {"ID": 1, "_id": 0})
        user_ids = [doc["ID"] async for doc in cursor]
        return user_ids
    
    except Exception as e:
        logger.error(f"❌ 查詢所有使用者 ID 失敗")
        return []
