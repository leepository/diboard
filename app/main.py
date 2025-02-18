import os

from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    Depends
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.config import get_config
from app.container import Container
from app.domains.domain_routers import domain_router
from app.domains.index.apis import index_router
from app.middlewares.token_validator_middleware import AccessControl
# from app.middlewares.token_validator_middleware import access_control
from app.utils.common_utils import get_ttl_hash, get_api_env

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Container setup
#     container = Container()
#     container.wire(modules=[__name__])
#
#     # Add container to app state
#     app.container = container
#
#     yield
#
#     # Cleanup
#     container.unwire()



def create_app(api_env: str = None):

    if api_env is not None:
        os.environ['API_ENV'] = api_env
    else:
        api_env = get_api_env()

    ttl_hash = get_ttl_hash()
    conf = get_config(api_env=api_env, ttl_hash=ttl_hash)

    container = Container()

    app = FastAPI(
        title="diBoard",
        version="v0.1.0-dev",
        contact={
            "name": "Kevin Lee",
            "email": "hleepublic@gmail.com"
        },
        docs_url="/docs",
        redoc_url="/redoc",
        debug=True,
        swagger_ui_parameters={"persistAuthorization": True},
        # lifespan=lifespan
    )

    app.container = container

    ## 미들웨어 등록
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts = conf.TRUSTED_HOSTS
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.add_middleware(AccessControl)

    ## Router 등록
    app.include_router(index_router)
    app.include_router(domain_router)

    if api_env != 'TEST':
        print(">>>>> Run Application <<<<<")
    return app
