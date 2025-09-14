from pydantic import BaseModel

class VerifyResponse(BaseModel):
    ID :str
    name :str 
    access_token :str
    
