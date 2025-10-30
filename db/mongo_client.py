import os 
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
ASSET_DB = os.getenv("ASSET_DB")

if not MONGO_URL:
    raise ValueError(" MONGO_URL 環境變數未設定，請檢查 .env 檔案")

client = AsyncIOMotorClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000,
    maxPoolSize=20,   # 最大連線數
    minPoolSize=5     # 最小連線數（啟動時就會建立）
)
asset_db = client[ASSET_DB]

def user_collection():
    return asset_db["user"]

def asset_collection():
    return asset_db["asset"]

def analyze_collection():
    return asset_db["analyze"]