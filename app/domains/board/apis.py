import urllib

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Path,
    Response,
    UploadFile
)
from fastapi_pagination import Params as PaginationParams
from starlette.requests import Request
from typing import List

from dependency_injector.wiring import inject, Provide
from app.container import Container
from app.domains.board.services import (
    ArticleService,
    AttachedFileService,
    CommentService,
    TagService
)
from app.domains.board.models import (
    Article,
    Comment
)
from app.domains.board.schemas import (
    ArticleBase,
    ArticleData,
    ArticleUpsert,
    CommentCreate,
    CommentData,
    ExecutionResult
)
from app.utils.debug_utils import dpp

board_router = APIRouter()

@board_router.get(
    name="Article 목록 조회",
    path="/articles",
    response_model=list[ArticleBase]
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
    result_service = article_service.get_article_list(
        page=pagination_param.page,
        size=pagination_param.size
    )
    return result_service

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

@board_router.post(
    name="Article 등록",
    path="/articles",
    response_model=ExecutionResult
)
@inject
async def create_article_api(
        data: ArticleUpsert = Depends(),
        files: List[UploadFile] = File(description="첨부파일", default=None),
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
    exec_result = await article_service.create_article(
        article=article,
        tag_data=tag_data,
        files=files
    )

    return {'result': exec_result}


@board_router.patch(
    name="Article 수정",
    path="/article/{article_id}",
    response_model=ExecutionResult
)
@inject
async def update_article_api(
        data: ArticleUpsert = Depends(),
        files: List[UploadFile] = File(description="첨부파일", default=None),
        article_id: int = Path(description="Article 일련 번호"),
        article_service: ArticleService = Depends(Provide[Container.article_service])
):
    """
    Article 수정
    """
    tag_data = data.tags
    result_service = await article_service.update_article(article_id=article_id, article_data=data, tag_data=tag_data, files=files)
    return {'result': result_service}


@board_router.delete(
    name="Article 삭제",
    path="/article/{article_id}",
    response_model=ExecutionResult
)
@inject
async def delete_article_api(
        article_id: int = Path(description="Article 일련 번호"),
        article_service: ArticleService = Depends(Provide[Container.article_service])
):
    """
    Article 삭제
    """
    result_service = article_service.delete_article(article_id=article_id)
    return {'result': result_service}


####################################################################################################################
# Article comment apis
####################################################################################################################
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
    response_model=ExecutionResult
)
@inject
async def create_comment_api(
        insert_data: CommentCreate,
        article_id: int = Path(description="Article 일련 번호"),
        comment_service: CommentService = Depends(Provide[Container.comment_service])
):
    """
    Comment 등록
    """
    result_service = comment_service.create_comment(insert_data, article_id)
    return {'result': result_service}

@board_router.patch(
    name="Comment 수정",
    path="/article/{article_id}/comment/{comment_id}",
    response_model=ExecutionResult
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
    result_service = comment_service.update_comment(
        article_id=article_id,
        comment_id=comment_id,
        update_data=update_data
    )
    return {'result': result_service}

@board_router.delete(
    name="Comment 삭제",
    path="/article/{article_id}/comment/{comment_id}",
    response_model=ExecutionResult
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
    result_service = comment_service.delete_comment(article_id=article_id, comment_id=comment_id)
    return {'result': result_service}

@board_router.delete(
    name="Comment 전체 삭제",
    path="/article/{article_id}/comment",
    response_model=ExecutionResult
)
@inject
async def delete_comment_all_api(
        article_id: int = Path(description="Article 일련 번호"),
        comment_service: CommentService = Depends(Provide[Container.comment_service])
):
    """
    Article 내 Comment 전체 삭제
    """
    result_service = comment_service.delete_comment_all(article_id=article_id)
    return {'result': result_service}


####################################################################################################################
# Artcle tag apis
####################################################################################################################
@board_router.delete(
    name="단일 Tag 삭제",
    path="/article/tag/{tag_id}",
    response_model=ExecutionResult
)
@inject
async def delete_tag_api(
        tag_id: int = Path(description="Tag 일련 번호"),
        tag_service: TagService = Depends(Provide[Container.tag_service])
):
    """
    단일 Tag 삭제
    """
    return tag_service.delete(tag_id=tag_id)


####################################################################################################################
# Attached file apis
####################################################################################################################
@board_router.get(
    name="첨부파일 다운로드",
    path="/article/{article}/attached-file/{attached_file_id}"
)
@inject
async def get_attached_file_download_api(
        attached_file_id: int = Path(description="첨부 파일 일련 번호"),
        attached_file_service: AttachedFileService = Depends(Provide[Container.attached_file_service])
):
    """
    첨부 파일 다운로드 API
    """
    contents, file_name = await attached_file_service.get_attached_file_download(
        attached_file_id=attached_file_id
    )

    return Response(
        content=contents,
        headers={
            'Content-Disposition': f'attachment;filename={urllib.parse.quote(file_name)}',
            'Content-Type': 'application/octet-stream;charset=UTF-8',
        }
    )