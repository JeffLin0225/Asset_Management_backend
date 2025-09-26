from pydantic import BaseModel
from typing import List

class Card(BaseModel):
    id :str             
    name :str 
    amount :int
    note :str
    order :int
    updatedTime :str

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

class Asset(BaseModel):
    userId :str
    asset :List[Category]