import redis
import os 
import asyncio
import json
from datetime import datetime
from fastapi.logger import logger

from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.from_url(REDIS_URL)

''' 把資料先存到 Redis '''
async def save_temp_assetData( userId:str , asset_data :str ):
    
    temp_asset_data_key = "last_data:"+userId
    temp_time_key = "debounce_timer:"+userId

    data_template = {
        "data" : asset_data ,
        "timestamp" : datetime.now().isoformat()
    }

    # 最新資料
    redis_client.setex( temp_asset_data_key , 30 , data_template )

    # 重新定時，TTL 
    redis_client.setex( temp_time_key , 5 , "timer" )

    ''' 還需要try catch '''

    return True

async def redis_subscribe_expired() -> str:
    pubsub = redis_client.pubsub()
    pubsub.subscribe("__keyevent@0__:expired")
 
    # 這是listener
    for message in pubsub.listen():
        if message['type'] == 'message':
            expired_key :str = message['data']
            if expired_key.startswith("debounce_timer:"):
                userid :str = expired_key[len("debounce_timer:"):]
                data_key :str = f"last_data:{userid}"
                data_value :str = redis_client.get(data_key)
                return data_value


@app.on_event("startup")
async def startup_event():
    # 啟動時檢查所有 latest_data:* key
    keys = redis_client.keys("latest_data:*")
    for key in keys:
        user_id = key[len("latest_data:"):]
        raw_data = redis_client.get(key)
        if raw_data:
            data_with_ts = json.loads(raw_data)
            
            #  這邊再丟給 mongo 存 await to_save_mongo 

    asyncio.create_task(redis_expired_subscriber())