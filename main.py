from fastapi import FastAPI ,HTTPException,Depends
from sqlalchemy.orm import Session
from models import Application , ApplicationCreate , ApplicationUpdate
from typing import Literal
from database import engine,Base,get_db
import db_models

Base.metadata.create_all(bind=engine)


app=FastAPI()


@app.get("/")
def home():
    return {"message":"Job Application Tracker API is live "}

@app.get("/applications",response_model=list[Application])
def list_applications(status:Literal["Applied","Interview","Offer","Rejected"] |None=None,db:Session=Depends(get_db)):
    query=db.query(db_models.ApplicationDB)
    if status is not None:
        query=query.filter(db_models.ApplicationDB.status==status)
    return query.all()
    
    
@app.get("/applications/{id}",response_model=Application)
def get_applications_by_id(id:int,db:Session=Depends(get_db)):
    row=db.query(db_models.ApplicationDB).filter(db_models.ApplicationDB.id==id).first()
    if row is None:
            raise HTTPException(status_code=404,detail="Application not found")
    return row
    

@app.post("/applications",status_code=201, response_model=Application)
def post_application(data:ApplicationCreate,db:Session=Depends(get_db)):
    new_row= db_models.ApplicationDB(company=data.company,role=data.role,status="Applied")
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row

@app.patch("/applications/{id}" ,response_model=Application)
def update_applicationstatus(id:int, data:ApplicationUpdate ,db:Session=Depends(get_db)):
    row=db.query(db_models.ApplicationDB).filter(db_models.ApplicationDB.id==id).first()
    if row is None:
        raise HTTPException(status_code=404,detail="Application not found")
    row.status=data.status
    db.commit()
    db.refresh(row)
    return row
  
@app.delete("/applications/{id}")
def delete_application(id:int,db:Session=Depends(get_db)):
    row=db.query(db_models.ApplicationDB).filter(db_models.ApplicationDB.id==id).first()
    if row is None:
        raise HTTPException(status_code=404,detail="Application not found")
    db.delete(row)
    db.commit()
    return {"message":"Application deleted"}

        

    


