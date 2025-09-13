from fastapi import FastAPI
from api import verify_api


app = FastAPI(title= "資產管理系統")

app.include_router(verify_api.router , prefix="/api" , tags=["驗證"])