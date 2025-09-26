from fastapi import APIRouter
from fastapi import HTTPException
from typing import List 
from fastapi.logger import logger

from model.asset_data import Category ,Asset

router = APIRouter()

@router.post("/saveAsset")
async def asset(jsonbody :Asset):
    try:
        # print([c.model_dump() for c in jsonbody])
        print(jsonbody.model_dump_json())
    except Exception as e:
        logger.exception("資料格式錯誤！")
        raise HTTPException(status_code=500 , detail="資料格式錯誤！") 
    