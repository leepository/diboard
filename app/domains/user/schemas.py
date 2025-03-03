from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

class UserCreate(BaseModel):
    username: str = Field(title="User name")
    password: str = Field(title="Password")

class UserData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(title="User 일련번호")
    username: str = Field(title="Username")
    password: str = Field(title="Password")
    created_at: datetime = Field(title="생성일")

class ExecutionResp(BaseModel):
    result: bool = Field(title="수행 결과")