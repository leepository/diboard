from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path
)
from fastapi_pagination import Params as PaginationParams

from dependency_injector.wiring import inject, Provide
from app.container import Container
from app.domains.board.services import ArticleService
from app.domains.board.models import Article
from app.domains.board.schemas import ArticleCreate, ArticleData

board_router = APIRouter()

@board_router.post(
    name="Article 등록",
    path="/articles",
    response_model=ArticleData
)
@inject
async def create_article_api(
        data: ArticleCreate,
        article_service: ArticleService = Depends(Provide[Container.article_service])
):
    """
    Article 등록 API
    """
    article = Article(**data.model_dump())
    return article_service.create_article(article=article)

@board_router.get(
    name="Article 목록 조회",
    path="/articles",
    response_model=list[ArticleData]
)
@inject
async def get_article_list_api(
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
