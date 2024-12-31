from datetime import datetime
from pydantic import BaseModel, Field

class ArticleCreate(BaseModel):
    title: str = Field(title="제목")
    content: str = Field(title="내용")

class ArticleData(BaseModel):
    id: int = Field(title="일련 번호")
    title: str = Field(title="제목")
    content: str = Field(title="내용")
    created_at: datetime = Field(title="작성일시")
