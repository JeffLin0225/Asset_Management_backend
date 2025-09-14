from fastapi import APIRouter
from model.user_info import UserInfo
from dto.verify_request import VerifyRequest
from dto.verify_response import VerifyResponse
from fastapi import HTTPException

from fastapi.logger import logger

from service.verify_service import verify_pin

router = APIRouter()

@router.post("/verify" , response_model=VerifyResponse)
async def verify(jsonbody : VerifyRequest ):

    try:
        verify_response :VerifyResponse = await verify_pin(jsonbody.ID,jsonbody.pin)
    except HTTPException as e:
        # 這是你自己丟的錯誤，直接重拋
        raise e
    except Exception as e :    
        logger.exception("驗證時發生錯誤！ ")
        raise HTTPException(status_code=500 , detail="驗證時發生錯誤！ ") 
    
    return verify_response