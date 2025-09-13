from pydantic import BaseModel

class VerifyRequest(BaseModel):
    ID: str
    pin: str