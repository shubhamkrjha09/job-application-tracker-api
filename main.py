from fastapi import FastAPI

app=FastAPI()

applications=[{"id":1,"company":"Google","role":"Intern","status":"Applied"},
              {"id":2,"company":"Amazon","role":"Backend developer","status":"Interview"}]

@app.get("/")
def home():
    return {"message":"Job Application Tracker API is live "}

@app.get("/applications")
def list_applications():
    return applications

