from fastapi import APIRouter
from model.user_info import UserInfo
from dto.verify_request import VerifyRequest
from service.verify_service import verify_pin

router = APIRouter()

@router.post("/verify" , response_model=UserInfo)
async def verify(jsonbody : VerifyRequest ):
    return await verify_pin(jsonbody.ID,jsonbody.pin)