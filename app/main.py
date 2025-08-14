from fastapi import FastAPI
from app.routers import admin, product

app = FastAPI(title="Zebrands")

versionAPI = "v1"
app.include_router(admin.router, prefix=f"/api/{versionAPI}/admin")
app.include_router(product.router, prefix=f"/api/{versionAPI}/product")


