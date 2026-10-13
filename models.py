from pydantic import BaseModel, Field
from typing import Literal

class Application(BaseModel):
    id:int
    company:str
    role:str
    status:Literal["Applied","Interview","Offer","Rejected"]

class ApplicationCreate(BaseModel):
    company:str=Field(min_length=1)
    role:str=Field(min_length=1)

class ApplicationUpdate(BaseModel):
    status:Literal["Applied","Interview","Offer","Rejected"]

