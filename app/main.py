from fastapi import FastAPI
from app.routers import admin, product
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Zebrands")

origins = [
    "http://localhost:5173", # Origin React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

version_api_v1 = "v1"
app.include_router(admin.router, prefix=f"/api/{version_api_v1}/admin")
app.include_router(product.router, prefix=f"/api/{version_api_v1}/product")
