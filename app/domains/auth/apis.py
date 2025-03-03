from dependency_injector.wiring import inject, Provide
from fastapi import (
    APIRouter,
    Depends
)

from app.domains.auth.schemas import AuthRequest, AuthResponse, ExecutionResp
from app.domains.auth.services import AuthService
from app.container import Container

auth_router = APIRouter()

@auth_router.post(
    name="Sign in",
    path="/signin",
    response_model=AuthResponse
)
@inject
async def signin_api(
        data: AuthRequest,
        auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    Signin API
    """
    return auth_service.signin(data=data)

@auth_router.post(
    name="Signout",
    path="/signout",
    response_model=ExecutionResp
)
@inject
async def signout_api(
        auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    """
    Signout API
    """
    return auth_service.signout()
