import json
import logging
from datetime import datetime
from fastapi.logger import logger
logger = logging.getLogger("uvicorn.error")  # 確保 log 出現在 console
from cache.redis_client import redis_client
 
''' 把資料先存到 Redis '''
async def save_asset_to_redis( userId:str , asset_data :dict ):
    
    temp_asset_data_key = "latest_data:"+userId
    temp_time_key = "debounce_timer:"+userId

    data_template = {
        "data" : asset_data ,
        "timestamp" : datetime.now().isoformat()
    }

    # 最新資料
    redis_client.setex( temp_asset_data_key , 30 , json.dumps(data_template) )

    # 重新定時，TTL 
    redis_client.setex( temp_time_key , 5 , "timer" )

    ''' 還需要try catch '''

    logger.info("已存入")

