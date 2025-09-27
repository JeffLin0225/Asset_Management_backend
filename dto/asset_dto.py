from pydantic import BaseModel
from typing import List

from model.asset_data import Category

class AssetRequest(BaseModel):
    userId :str
    asset :List[Category]

# class AssetResponse(BaseModel):