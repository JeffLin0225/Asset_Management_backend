
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.logger import logger

from service.auth import verify_token
from model.copy_token import CopyRequest
from service.analyze_service import copy_asset_info_analyze , find_analyze_info , batch_copy_analyze
import os 
from dotenv import load_dotenv

load_dotenv()
COPY_SECRET_KEY = os.getenv("COPY_SECRET_KEY")

router = APIRouter()

@router.get("/getAnalyze")
async def getAnalyze(userId :str , _=Depends(verify_token)):
    try:
        print(userId)
        result = await find_analyze_info( userId )
        
        return result
    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！")
    
@router.get("/manualcopyAnalyze")
async def manualcopyAnalyze( userId :str ):
    try:
        print(userId)
        result = await copy_asset_info_analyze(userId)
        
        return result
    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    
@router.post("/copyAnalyze")
async def copyAnalyze(req :CopyRequest):

    if req.token != COPY_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await batch_copy_analyze()
    return result