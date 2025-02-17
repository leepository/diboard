from dependency_injector.wiring import inject, Provide
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path
)
from fastapi_pagination import Params as PaginationParams
from typing import List

from app.domains.user.models import User
from app.domains.user.schemas import (
    ExecutionResp,
    UserCreate,
    UserData
)
from app.domains.user.services import UserService
from app.container import Container

user_router = APIRouter()

@user_router.get(
    name="User 목록 조회",
    path="/users",
    response_model=List[UserData]
)
@inject
async def get_user_list_api(
        pagination_params: PaginationParams = Depends(),
        user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    User 목록 조회 API
    """
    return user_service.get_list(
        page=pagination_params.page,
        size=pagination_params.size
    )

@user_router.get(
    name="User 상세 조회",
    path="/user/{user_id}",
    response_model=UserData
)
@inject
async def get_user_detail_api(
        user_id: int = Path(description="User 일련 번호"),
        user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    User 상세 조회
    """
    user = user_service.get_detail(user_id=user_id)
    return user


@user_router.post(
    name="User 생성",
    path="/user",
    response_model=UserData
)
@inject
async def create_user_api(
        data: UserCreate,
        user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    신규 User 생성
    """
    user = User(**data.model_dump())
    return user_service.create_user(user=user)

@user_router.delete(
    name="User 삭제",
    path="/user/{user_id}",
    response_model=ExecutionResp
)
@inject
async def delete_user_api(
        user_id: int = Path(description="User 일련 번호"),
        user_service: UserService = Depends(Provide[Container.user_service])
):
    """
    User 삭제
    """
    result = user_service.delete_user(user_id=user_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User is not found"
        )
    return user_service

