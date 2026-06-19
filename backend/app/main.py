from fastapi import FastAPI

app = FastAPI(title="Lead & Customer Management System API")

@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI Backend"}
