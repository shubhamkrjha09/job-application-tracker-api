from fastapi import FastAPI ,HTTPException
from models import Application


app=FastAPI()

applications=[Application(id=1,company="Google",role="Intern",status="Applied"),
              Application(id=2,company="Amazon",role="Backend developer",status="Interview")
              ]

@app.get("/")
def home():
    return {"message":"Job Application Tracker API is live "}

@app.get("/applications")
def list_applications():
    return applications


@app.get("/applications/{id}")
def get_applications_by_id(id:int):
    for application in applications:
        if application.id == id:
            return application
    raise HTTPException(status_code=404,detail="Application not found")  

