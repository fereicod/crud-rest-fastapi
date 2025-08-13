from fastapi import FastAPI
from app.routers import admin

app = FastAPI(title="Zebrands")

app.include_router(admin.router, prefix="/admin")

@app.get('/')
def root():
    return {"message":"hello"}


