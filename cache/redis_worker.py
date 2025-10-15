import logging
import os
import asyncio
import json
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from redis import asyncio as aioredis   # ✅ 正確的 async redis import

from db.mongo_repository import save_asset

logger = logging.getLogger("uvicorn.error")

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

redis_client: aioredis.Redis | None = None

async def redis_subscribe_expired():
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe("__keyevent@*__:expired")

    async for message in pubsub.listen():
        logger.info(f"收到 pubsub 訊息: {message}")
        if message["type"] in ("message", "pmessage"):
            expired_key: str = message["data"]
            if expired_key.startswith("debounce_timer:"):
                userid: str = expired_key[len("debounce_timer:"):]
                data_key: str = f"latest_data:{userid}"
                data_value = await redis_client.get(data_key)
                if data_value:
                    parsed = json.loads(data_value)
                    payload = parsed.get("data")
                    logger.info("redis 過期資料存入 DB：" + json.dumps(payload, ensure_ascii=False))
                    await save_asset(payload["userId"], payload["asset"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

    try:
        await redis_client.config_set("notify-keyspace-events", "Ex")
        logger.info("已設定 notify-keyspace-events = Ex")
    except Exception as e:
        logger.warning(f"設定 notify-keyspace-events 失敗：{e}")

    async for key in redis_client.scan_iter("latest_data:*"):
        user_id = key[len("latest_data:"):]
        raw_data = await redis_client.get(key)
        if raw_data:
            data_with_ts = json.loads(raw_data)
            logger.info("啟動的過期資料：" + str(data_with_ts))
            try:
                await save_asset(data_with_ts["userId"], data_with_ts["asset"])
                logger.info("存入 DB 了")
            except Exception:
                logger.exception(f"{user_id}: 儲存 DB 失敗")

    asyncio.create_task(redis_subscribe_expired())
    yield
    await redis_client.close()
