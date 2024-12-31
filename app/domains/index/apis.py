import os

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

index_router = APIRouter()

@index_router.get(
    path="/",
    name="Application index",
    response_class=PlainTextResponse
)
async def index_api():
    """ Application index api """
    api_env = os.getenv("API_ENV", "DEV")
    return f"[{api_env}] Application started ...."

@index_router.get(
    path="/health",
    name="Application health check api",
    response_class=PlainTextResponse
)
async def application_health_check_api():
    """ Application health check api """
    return "OK"
