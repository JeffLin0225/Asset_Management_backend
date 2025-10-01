from fastapi.logger import logger
from db.mongo_client import asset_collection

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
