from fastapi import FastAPI ,HTTPException,Depends
from sqlalchemy.orm import Session
from models import Application , ApplicationCreate , ApplicationUpdate
from typing import Literal
from database import engine,Base,get_db
import db_models

Base.metadata.create_all(bind=engine)


app=FastAPI()

applications=[Application(id=1,company="Google",role="Intern",status="Applied"),
              Application(id=2,company="Amazon",role="Backend developer",status="Interview")
              ]

@app.get("/")
def home():
    return {"message":"Job Application Tracker API is live "}

@app.get("/applications",response_model=list[Application])
def list_applications(db:Session=Depends(get_db)):
    rows=db.query(db_models.ApplicationDB).all()
    return rows
    

    
@app.get("/applications/{id}")
def get_applications_by_id(id:int):
    for application in applications:
        if application.id == id:
            return application
    raise HTTPException(status_code=404,detail="Application not found") 

def get_next_id():
    if not applications:
        return 1
    biggest=0
    for application in applications:
        if application.id>biggest:
            biggest=application.id
    return biggest+1 

@app.post("/applications",status_code=201, response_model=Application)
def post_application(data:ApplicationCreate,db:Session=Depends(get_db)):
    new_row= db_models.ApplicationDB(company=data.company,role=data.role,status="Applied")
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row

@app.patch("/applications/{id}")
def update_applicationstatus(id:int,data:ApplicationUpdate):
    for application in applications:
        if application.id== id:
            application.status=data.status
            return application
    raise HTTPException(status_code=404,detail="Application not found")

@app.delete("/applications/{id}")
def delete_application(id:int):
    for application in applications:
        if application.id==id:
            applications.remove(application)
            return {"message":"Application deleted"}
    raise HTTPException(status_code=404,detail="Application not found")


