from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import models
from database import engine
from routers import auth_router, comics_router
from rate_limiter import limiter

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Comic Collection Secure API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:3000",
    "https://placeholderformydomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router.router)
app.include_router(comics_router.router)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Database connected and API running"}