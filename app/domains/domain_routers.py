from fastapi import APIRouter, Depends

from app.common.constants import API_KEY_HEADER
from app.domains.auth.apis import auth_router
from app.domains.board.apis import board_router
from app.domains.user.apis import user_router

domain_router = APIRouter()
domain_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)
domain_router.include_router(
    board_router,
    prefix="/board",
    tags=["Board"],
    dependencies=[Depends(API_KEY_HEADER)]
)
domain_router.include_router(
    user_router,
    prefix="/membership",
    tags=["User"],
    # dependencies=[Depends(API_KEY_HEADER)]
)