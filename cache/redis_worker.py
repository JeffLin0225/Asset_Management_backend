import logging
from fastapi import FastAPI
import redis
import os 
import asyncio
import json
from datetime import datetime
logger = logging.getLogger("uvicorn.error")  # 確保 log 出現在 console

from cache.redis_client import redis_client
from db.mongo_repository import save_asset

from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.from_url(REDIS_URL) # connectuion ppool 

async def redis_subscribe_expired():
    pubsub = redis_client.pubsub()
    pubsub.psubscribe("__keyevent@*__:expired")  # ✅ 監聽所有 DB 的 expired

    def _listen():
        # 這是listener
        for message in pubsub.listen():
            logger.info(f"收到 pubsub 訊息: {message}")  # ✅ debug
            if message['type'] in ('message', 'pmessage'):
                expired_key :str = message['data']
                expired_key = expired_key.decode("utf-8")
                if expired_key.startswith("debounce_timer:"):
                    userid :str = expired_key[len("debounce_timer:"):]
                    data_key :str = f"latest_data:{userid}"
                    data_value :str = redis_client.get(data_key)
                    logger.info("過期資料存入："+data_value.decode("utf-8"))
    await asyncio.to_thread(_listen)

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        redis_client.config_set("notify-keyspace-events", "Ex")
        logger.info("已設定 notify-keyspace-events = Ex")
    except Exception as e:
        logger.warning(f"設定 notify-keyspace-events 失敗：{e}")

    # 讀出設定確認
    try:
        current = redis_client.config_get("notify-keyspace-events").get("notify-keyspace-events", "")
        db_index = redis_client.connection_pool.connection_kwargs.get("db")
        logger.info(f"目前通知設定: '{current}', 使用 DB 索引: {db_index}")
    except Exception as e:
        logger.warning(f"讀取通知設定失敗：{e}")

    # 啟動時檢查所有 latest_data:* key
    keys = redis_client.scan_iter("latest_data:*")
    for key in keys:
        if isinstance(key, bytes):
            key = key.decode("utf-8")
        user_id = key[len("latest_data:"):]
        raw_data = redis_client.get(key)
        if raw_data:
            data_with_ts = json.loads(raw_data.decode("utf-8"))
            logger.info("啟動的過期資料：" + str(data_with_ts))
            
            # 儲存mongo DB
            try:
                await save_asset(data_with_ts)
                logger.info("存入ＤＢ了")
            except:
                logger.exception(f'{user_id}:儲存DB失敗')    

    asyncio.create_task(redis_subscribe_expired())
    yield

    redis_client.close()   # ✅ 同步 client 不要 await
