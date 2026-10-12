from pydantic import BaseModel

class Application(BaseModel):
    id:int
    company:str
    role:str
    status:str
    

