from app.domains.auth.schemas import AuthRequest
from app.domains.auth.handlers import AuthHandler

class AuthService:
    def __init__(self, auth_handler: AuthHandler):
        self._handler = auth_handler

    def signin(self, data: AuthRequest):
        pass