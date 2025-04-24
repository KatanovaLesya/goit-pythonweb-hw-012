"""
Точка входу до REST API застосунку GoIT Contacts.

Запускає FastAPI сервер із підключеними роутами.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2

from routers.auth_router import router as auth_router
from routers.contacts import router as contacts_router


from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from rate_limiter import limiter
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from database import DATABASE_URL


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)

app = FastAPI(
    title="Contacts API",
    description="REST API для керування контактами",
    version="1.0.0",
    openapi_tags=[{"name": "auth", "description": "Аутентифікація"}]
)

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print("🚀 Using DB:", DATABASE_URL)

    redis_connection = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router, prefix="/auth")
app.include_router(contacts_router)


@app.get("/")
def root():
    return {"message": "Welcome to HW10 API"}



