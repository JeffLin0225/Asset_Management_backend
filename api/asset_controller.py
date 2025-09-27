from fastapi import APIRouter
from fastapi import HTTPException
from typing import List 
from fastapi.logger import logger

from dto.asset_dto import AssetRequest
from service.asset_service import save_user_asset_info

router = APIRouter()

@router.post("/saveAsset")
async def asset(jsonbody :AssetRequest ):
    try:
        # print([c.model_dump() for c in jsonbody])
        print(jsonbody.model_dump_json())
        await save_user_asset_info( jsonbody.userId  , jsonbody.model_dump() )

    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    