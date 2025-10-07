
from fastapi import APIRouter
from fastapi import HTTPException
from typing import List 
from fastapi.logger import logger

from dto.asset_dto import AssetRequest
from service.analyze_service import copy_asset_info

router = APIRouter()

@router.get("/getAnalyze")
async def getAnalyze(userId :str ):
    try:
        print(userId)
        return await copy_asset_info( userId )
    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    

# @router.post("/saveAsset")
# async def saveAsset(jsonbody :AssetRequest ):
#     try:
#         print(jsonbody.model_dump_json())
#         await save_temporary_asset( jsonbody.userId  , jsonbody.model_dump() )

#     except Exception as e:
#         logger.exception("資料格式錯誤！")
#         raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    