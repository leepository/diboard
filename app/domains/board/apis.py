from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Path,
    UploadFile
)
from fastapi_pagination import Params as PaginationParams
from starlette.requests import Request
from typing import List

from dependency_injector.wiring import inject, Provide
from app.container import Container
from app.domains.board.services import (
    ArticleService,
    CommentService
)
from app.domains.board.models import (
    Article,
    Comment
)
from app.domains.board.schemas import (
    ArticleCreate,
    ArticleData,
    CommentCreate,
    CommentData,
    ExecutionResult
)

board_router = APIRouter()

@board_router.post(
    name="Article 등록",
    path="/articles",
    response_model=ExecutionResult
)
@inject
async def create_article_api(
        data: ArticleCreate,
        files: List[UploadFile] = File(default=..., description="첨부파일"),
        article_service: ArticleService = Depends(Provide[Container.article_service])
):
    """
    Article 등록 API
    """
    article = Article(
        title=data.title,
        content=data.content
    )
    tag_data = article.tags
    exec_result = article_service.create_article(article=article, tag_data=tag_data)

    return {'result': exec_result}

@board_router.get(
    name="Article 목록 조회",
    path="/articles",
    response_model=list[ArticleData]
)
@inject
async def get_article_list_api(
        request: Request,
        pagination_param: PaginationParams = Depends(),
        article_service: ArticleService = Depends(Provide[Container.article_service])
):
    """
    Article 목록 조회 API
    """
    return article_service.get_article_list(
        page=pagination_param.page,
        size=pagination_param.size
    )

@board_router.get(
    name="Article 상세 조회",
    path="/article/{article_id}",
    response_model=ArticleData
)
@inject
async def get_article_detail_api(
        article_id: int = Path(description="Article 일련 번호"),
        article_service: ArticleService = Depends(Provide[Container.article_service])
):
    """
    Article 상세 조회 API
    """
    article = article_service.get_article_detail(article_id=article_id)
    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )
    return article

@board_router.put(
    name="Article 수정",
    path="/article/{article_id}",
    response_model=ExecutionResult
)
@inject
async def update_article_api(
        data: ArticleCreate,
        article_id: int = Path(description="Article 일련 번호"),
        article_service: ArticleService = Depends(Provide[Container.article_handler])
):
    """
    Article 수정
    """
    tag_data = data.tags
    article = article_service.update_article(article_id=article_id, article_data=data, tag_data=tag_data)
    return article

@board_router.delete(
    name="Article 삭제",
    path="/article/{article_id}",
    response_model=ArticleData
)
@inject
async def delete_article_api(
        article_id: int = Path(description="Article 일련 번호"),
        article_service: ArticleService = Depends(Provide[Container.article_service])
):
    """
    Article 삭제
    """
    return article_service.delete_article(article_id=article_id)



## For Comment
@board_router.get(
    name="Comment 목록 조회",
    path="/article/{article_id}/comments",
    response_model=list[CommentData]
)
@inject
async def get_comment_list_api(
        article_id: int = Path(description="Article 일련 번호"),
        pagination_params: PaginationParams = Depends(),
        comment_service: CommentService = Depends(Provide[Container.comment_service])
):
    """
    Comment 목록 조회 API
    """
    return comment_service.get_comment_list(
        article_id=article_id,
        page=pagination_params.page,
        size=pagination_params.size
    )

@board_router.get(
    name="Comment 상세 조회",
    path="/article/{article_id}/comment/{comment_id}",
    response_model=CommentData
)
@inject
async def get_comment_detail_api(
        article_id: int = Path(description="Article 일련 번호"),
        comment_id: int = Path(description="Comment 일련 번호"),
        comment_service: CommentService = Depends(Provide[Container.comment_service])
):
    """
    Comment 상세 조회 API
    """
    return comment_service.get_comment_detail(comment_id=comment_id)

@board_router.post(
    name="Comment 등록",
    path="/article/{article_id}/comment",
    response_model=CommentData
)
@inject
async def create_comment_api(
        post_data: CommentCreate,
        article_id: int = Path(description="Article 일련 번호"),
        comment_service: CommentService = Depends(Provide[Container.comment_service])
):
    """
    Comment 등록
    """
    comment = Comment(**post_data.data_dump())
    return comment_service.create_comment(comment, article_id)

@board_router.patch(
    name="Comment 수정",
    path="/article/{article_id}/comment/{comment_id}",
    response_model=CommentData
)
@inject
async def update_comment_api(
        update_data: CommentCreate,
        article_id: int = Path(description="Article 일련 번호"),
        comment_id: int = Path(description="Comment 일련 번호"),
        comment_service: CommentService = Depends(Provide[Container.comment_service])
):
    """
    Comment 수정
    """
    return comment_service.update_comment(
        article_id=article_id,
        comment_id=comment_id,
        update_data=update_data
    )

@board_router.delete(
    name="Comment 삭제",
    path="/article/{article_id}/comment/{comment_id}",
    response_model=CommentData
)
@inject
async def delete_comment_api(
        article_id: int = Path(description="Article 일련 번호"),
        comment_id: int = Path(description="Comment 일련 번호"),
        comment_service: CommentService = Depends(Provide[Container.comment_service])
):
    """
    Comment 삭제
    """
    return comment_service.delete_comment(article_id=article_id, comment_id=comment_id)
