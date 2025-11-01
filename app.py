from fastapi import FastAPI
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from api import login_controller , asset_controller , analyze_controller
from cache.redis_worker import lifespan   

load_dotenv()

app = FastAPI(title= "資產管理系統",lifespan=lifespan)

origins = os.getenv("CORS_ORIGINS", "").split(",")
print("環境參數:"+origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_controller.router , prefix="/api" , tags=["驗證"])
app.include_router(asset_controller.router , prefix="/api" , tags=["資產"])
app.include_router(analyze_controller.router , prefix="/api" , tags=["分析"])