from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import login_controller


app = FastAPI(title= "資產管理系統")

# 允許的來源
origins = [
    "http://localhost:5173",  # 開發環境
    "http://127.0.0.1:5173",  # 正式環境
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 允許的來源
    allow_credentials=True,         # 是否允許 cookie
    allow_methods=["*"],             # 允許的 HTTP 方法
    allow_headers=["*"],             # 允許的 HTTP Header
)

app.include_router(login_controller.router , prefix="/api" , tags=["驗證"])