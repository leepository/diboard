from dataclasses import dataclass
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from app.domains.board.models import Article

class ExecutionResult(BaseModel):
    result: bool = Field(title="수행 결과")

## For Article
@dataclass
class ArticleUpsert:
    title: str = Form(title="제목", default=None)
    content: str = Form(title="내용", default=None)
    tags: Optional[List[str]|None] = Form(title="Tag", default=None)


class ArticleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(title="일련 번호")
    title: str = Field(title="제목")
    content: str = Field(title="내용")
    created_at: datetime = Field(title="작성일시")
    updated_at: datetime = Field(title="수정일시")

class TagBase(BaseModel):
    id: int = Field(title="일련 번호")
    tagging: str = Field(title="Tag 내용")

class AttachedFileBase(BaseModel):
    id: int = Field(title="일련 번호")
    filename: str = Field(title="File name")
    file_size: int = Field(title="File size")
    file_type: str = Field(title="File type")

class ArticleData(ArticleBase):
    tags: List[TagBase] = Field(title="Tags", default=None)
    attached_files: List[AttachedFileBase] = Field(title="Attached_files", default=None)

## For Comment
class CommentCreate(BaseModel):
    article_id: int = Field(title="게시글 일련 번호")
    content: str = Field(title="댓글 내용")
    comment_id: int = Field(title="부모 댓글 일련 번호", default=None)

class CommentData(BaseModel):
    id: int = Field(title="댓글 일련 번호")
    article_id: int = Field(title="Article 일련번호")
    comment_id: Optional[int|None] = Field(title="부모 댓글 일련 번호")
    content: str = Field(title="댓글 내용")
    level: int = Field(title="댓글 레벨")
    created_at: datetime = Field(title="작성일")
    updated_at: datetime = Field(title="수정일")
