from fastapi import FastAPI

app = FastAPI(title="Zebrands")

@app.get('/')
def root():
    return {"message":"hello"}


