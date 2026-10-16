from sqlalchemy import Integer,Column,String
from database import Base

class ApplicationDB(Base):
    __tablename__="applications"
    id=Column(Integer,primary_key=True,index=True)
    company=Column(String,nullable=False)
    role=Column(String,nullable=False)
    status=Column(String,nullable=False,default="Applied")


