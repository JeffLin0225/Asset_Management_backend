from pydantic import BaseModel

class UserInfo(BaseModel):
    ID :str
    name :str

