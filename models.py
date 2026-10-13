from pydantic import BaseModel
from typing import Literal

class Application(BaseModel):
    id:int
    company:str
    role:str
    status:Literal["Applied","Interview","Offer","Rejected"]

class ApplicationCreate(BaseModel):
    company:str
    role:str
class ApplicationUpdate(BaseModel):
    status:Literal["Applied","Interview","Offer","Rejected"]

