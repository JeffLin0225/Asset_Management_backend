from pydantic import BaseModel
class CopyRequest(BaseModel):
    token: str