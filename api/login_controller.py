from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.logger import logger

from dto.login_dto import LoginRequest , LoginResponse
from service.login_service import verify_pin

router = APIRouter()

@router.post("/login" , response_model=LoginResponse)
async def verify(jsonbody :LoginRequest ):

    try:
        verify_response :LoginRequest = await verify_pin(jsonbody.ID,jsonbody.pin)
    except HTTPException as e:
        # 丟的錯誤，直接重拋
        raise e
    except Exception as e :    
        logger.exception("驗證時發生錯誤！ ")
        raise HTTPException(status_code=500 , detail="驗證時發生錯誤！ ") 
    
    return verify_response