from fastapi import FastAPI
from app.routers import admin, product

app = FastAPI(title="Zebrands")

app.include_router(admin.router, prefix="/admin")
app.include_router(product.router, prefix="/product")

