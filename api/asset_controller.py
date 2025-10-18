from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.logger import logger

from dto.asset_dto import AssetRequest
from service.asset_service import find_user_asset_info , save_temporary_asset

router = APIRouter()

@router.get("/getAsset")
async def getAsset(userId :str ):
    try:
        print(userId)
        return await find_user_asset_info( userId )
    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    

@router.post("/saveAsset")
async def saveAsset(jsonbody :AssetRequest ):
    try:

        await save_temporary_asset( jsonbody.userId  , jsonbody.model_dump() )

    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    