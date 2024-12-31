import os

from fastapi import (
    FastAPI,
    Depends
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.common.config import get_config
from app.container import Container
from app.domains.domain_routers import domain_router
from app.domains.index.apis import index_router
from app.utils.common_utils import get_ttl_hash

def create_app():

    api_env = os.getenv("API_ENV", "DEV")
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
        debug=True
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

    ## Router 등록
    app.include_router(index_router)
    app.include_router(domain_router)

    print(">>>>> Run Application <<<<<")
    return app
