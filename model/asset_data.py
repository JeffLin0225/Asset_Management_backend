from pydantic import BaseModel , field_validator
from typing import List

class Card(BaseModel):
    id :str             
    name :str 
    amount :int
    note :str
    order :int
    updatedTime :str

    @field_validator("amount" , mode="before")
    def normalize_amount(cls , v):
        if v == "" or v is None:
            return 0 
        return v 
        
class SubCategory(BaseModel):
    id :str
    title :str
    order :int
    updatedTime :str  
    cardList :List[Card]

class Category(BaseModel):
    id :str
    title :str
    order :int
    updatedTime :str  
    subCategoryList :List[SubCategory]