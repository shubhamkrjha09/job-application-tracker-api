from fastapi import FastAPI ,HTTPException
from models import Application , ApplicationCreate , ApplicationUpdate


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

def get_next_id():
    if not applications:
        return 1
    biggest=0
    for application in applications:
        if application.id>biggest:
            biggest=application.id
    return biggest+1 

@app.post("/applications",status_code=201)
def post_application(data:ApplicationCreate):
    new_application=Application(id=get_next_id(),company=data.company,role=data.role,status="Applied")
    applications.append(new_application)
    return new_application
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


