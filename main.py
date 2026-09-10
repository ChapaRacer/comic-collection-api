from fastapi import FastAPI
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Comic Collection Secure API")

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Database connected and API running"}