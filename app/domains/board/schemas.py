from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

class ExecutionResult(BaseModel):
    result: bool = Field(title="수행 결과")

## For Article
class ArticleCreate(BaseModel):
    title: str = Field(title="제목")
    content: str = Field(title="내용")
    tags: List[str] = Field(title="Tag", default=None)

class ArticleData(BaseModel):
    id: int = Field(title="일련 번호")
    title: str = Field(title="제목")
    content: str = Field(title="내용")
    created_at: datetime = Field(title="작성일시")

## For Comment
class CommentCreate(BaseModel):
    article_id: int = Field(title="게시글 일련 번호")
    content: str = Field(title="댓글 내용")

class CommentData(BaseModel):
    id: int = Field(title="댓글 일련 번호")
    comment_id: int = Field(title="부모 댓글 일련 번호")
    content: str = Field(title="댓글 내용")
    level: int = Field(title="댓글 레벨")
    created_at: datetime = Field(title="작성일")
    updated_at: datetime = Field(title="수정일")
