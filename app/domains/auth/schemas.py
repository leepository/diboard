from pydantic import (
    BaseModel,
    Field
)

class AuthRequest(BaseModel):
    signin_id: str = Field(title="signin ID")
    signin_pass: str = Field(title="signin Password")

class AuthResponse(BaseModel):
    access_token: str = Field(title="Access token")
    refresh_token: str = Field(title="Refresh token")
