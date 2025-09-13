import os 
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
USER_DB = os.getenv("ASSET_DB")

if not MONGO_URL:
    raise ValueError(" MONGO_URL 環境變數未設定，請檢查 .env 檔案")

client = AsyncIOMotorClient(MONGO_URL , serverSelectionTimeoutMS=5000)
userdb = client[USER_DB]

def get_collection(collection_name :str):
    return userdb[collection_name]