from pydantic import BaseModel

class LoginRequest(BaseModel):
    ID :str
    pin :str

class LoginResponse(BaseModel):
    ID :str
    name :str
    access_token :str