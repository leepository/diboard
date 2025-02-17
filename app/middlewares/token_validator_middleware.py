import inspect
import re
import time

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Callable

from app.common.exceptions import exception_handler, APIException
from app.container import Container
from app.domains.auth.handlers import AuthHandler
from app.domains.user.handlers import UserHandler
from app.middlewares import except_paths
from app.utils.log_utils import api_logger

async def url_pattern_match(path: str, pattern: str):
    result = re.match(pattern, path)
    if result:
        return True
    return False

class AccessControl(BaseHTTPMiddleware):
    @inject
    def __init__(
            self,
            app: FastAPI,
            auth_handler: AuthHandler = Provide[Container.auth_handler],
            user_handler: UserHandler = Provide[Container.user_handler]
    ):
        super().__init__(app)
        self.auth_handler = auth_handler
        self.user_handler = user_handler

    async def dispatch(
            self,
            request: Request,
            call_next: Callable
    ):
        request.state.start_time = time.time()

        ip = request.headers['x-forwarded-for'] if "x-forwarded-for" in request.headers.keys() else request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip

        headers = request.headers
        url = request.url.path

        # Root 접근은 bypass
        if url == "/":
            response = await call_next(request)
        else:

            # 인증이 필요 없는 API의 경우에 대한 처리
            if await url_pattern_match(url, except_paths.EXCEPT_PATH_REGEX):
                try:
                    response = await call_next(request)
                    await api_logger(request=request, response=response)
                except Exception as ex:
                    error = await exception_handler(ex) if type(ex) is not APIException else ex
                    response = JSONResponse(status_code=error.status_code, content=error.detail)
                    await api_logger(request=request, error=error)

            else:
                # 인증이 필요한 API의 경우에 대한 처리
                try:
                    if "authorization" in headers.keys():
                        tmp_token = headers.get("authorization")
                        if tmp_token is None:
                            raise Exception("Access token required")
                        if not tmp_token.startswith("Bearer "):
                            raise Exception("Invalid token type - not Bearer token")
                        raw_token = tmp_token.replace("Bearer ", "")
                        user_id = self.auth_handler.decode_access_token(token=raw_token)
                        token_value = self.auth_handler.get_access_token_value(token=raw_token)
                        if token_value is None:
                            raise Exception("Invalid access token")
                        if user_id != token_value:
                            raise Exception("Invalid access token")
                        user = self.user_handler.get_detail(user_id = token_value)
                        request.state.user = user

                    else:
                        raise Exception("Authorization required")

                    response = await call_next(request)
                    await api_logger(request=request, response=response)

                except Exception as ex:
                    error = await exception_handler(ex) if type(ex) is not APIException else ex
                    response = JSONResponse(status_code=error.status_code, content=error.detail)
                    await api_logger(request=request, error=error)

        return response


# class AccessControl:
#     def __init__(self, container: Container):
#         self.container = container
#
#     @inject
#     async def __call(
#             self,
#             request: Request,
#             call_next: Callable,
#             auth_handler: AuthHandler = Provide[Container.auth_handler],
#             user_handler: UserHandler = Provide[Container.user_handler]
#     ):
#         print("start middleware --->")
#         request.state.start_time = time.time()
#
#         ip = request.headers['x-forwarded-for'] if "x-forwarded-for" in request.headers.keys() else request.client.host
#         request.state.ip = ip.split(",")[0] if "," in ip else ip
#
#         headers = request.headers
#         url = request.url.path
#
#         # Root 접근은 bypass
#         if url == "/":
#             response = await call_next(request)
#         else:
#
#             # 인증이 필요 없는 API의 경우에 대한 처리
#             if await url_pattern_match(url, except_paths.EXCEPT_PATH_REGEX):
#                 try:
#                     response = await call_next(request)
#                     await api_logger(request=request, response=response)
#                 except Exception as e:
#                     error = await exception_handler(e)
#                     response = JSONResponse(status_code=error.status_code, content=error.detail)
#                     await api_logger(request=request, error=error)
#
#             else:
#                 # 인증이 필요한 API의 경우에 대한 처리
#                 try:
#                     if "authorization" in headers.keys():
#                         tmp_token = headers.get("authorization")
#                         if tmp_token is None:
#                             raise Exception("Access token required")
#                         if not tmp_token.startswith("Bearer "):
#                             raise Exception("Invalid token type - not Bearer token")
#                         raw_token = tmp_token.replace("Bearer ", "")
#                         user_id = auth_handler.decode_access_token(token=raw_token)
#                         token_value = auth_handler.get_access_token_value(token=raw_token)
#                         if token_value is None:
#                             raise Exception("Invalid access token")
#                         if user_id != token_value:
#                             raise Exception("Invalid access token")
#                         user = user_handler.get_detail(user_id = token_value)
#                         print("user : ", user)
#                         request.state.user = user
#
#                     else:
#                         raise Exception("Authorization required")
#
#                     response = await call_next(request)
#                     await api_logger(request=request, response=response)
#
#                 except Exception as e:
#                     error = await exception_handler(e)
#                     response = JSONResponse(status_code=error.status_code, content=error.detail)
#                     await api_logger(request=request, error=error)
#
#         return response