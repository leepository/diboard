from fastapi import APIRouter

from app.domains.board.apis import board_router

domain_router = APIRouter()
domain_router.include_router(
    board_router,
    prefix="/board",
    tags=["Board"]
)
