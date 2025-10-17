
from fastapi import APIRouter
from fastapi import HTTPException
from typing import List 
from fastapi.logger import logger

from dto.asset_dto import AssetRequest
from service.analyze_service import copy_asset_info_analyze , find_analyze_info

router = APIRouter()

@router.get("/getAnalyze")
async def getAnalyze(userId :str ):
    try:
        print(userId)
        result = await find_analyze_info( userId )
        
        return [result]
    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！")
    

@router.get("/copyAnalyze")
async def copyAnalyze(userId :str ):
    try:
        print(userId)
        result = await copy_asset_info_analyze(userId)
        
        return result
    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    