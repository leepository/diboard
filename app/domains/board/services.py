from fastapi import UploadFile
from typing import List

from app.common.constants import S3_BUCKET, S3_KEY_PREFIX
from app.databases.transactions import TransactionManager
from app.domains.board.exceptions import (
    NotExistArticle,
    NotExistAttachedFile,
    NotExistComment,
    NotExistTag
)
from app.domains.board.models import (
    Article,
    AttachedFile,
    Comment,
    Tag
)
from app.domains.board.handlers import (
    ArticleHandler,
    AttachedFileHandler,
    CommentHandler,
    TagHandler
)
from app.domains.board.schemas import (
    ArticleUpsert,
    CommentCreate
)
from app.utils.debug_utils import dpp

class ArticleService:

    def __init__(
            self,
            article_handler: ArticleHandler,
            attached_file_handler: AttachedFileHandler,
            comment_handler: CommentHandler,
            tag_handler: TagHandler,
            transaction_manager: TransactionManager):
        self.article_handler = article_handler
        self.attached_file_handler = attached_file_handler
        self.comment_handler = comment_handler
        self.tag_handler = tag_handler
        self.transaction_manager = transaction_manager

    def get_article_list(self, page: int, size: int):
        return self.article_handler.get_list(page=page, size=size)

    def get_article_detail(self, article_id: int):
        article = self.article_handler.get_detail(article_id=article_id)
        if article is None:
            raise NotExistArticle()

        tags = self.tag_handler.get_list(article_id=article.id)
        article.tags = tags

        return article

    async def create_article(self, article: Article, tag_data: List[str], files: List[UploadFile] = None) -> bool:
        with self.transaction_manager.transaction():
            # create article
            article = self.article_handler.create(article=article)

            # create tags
            if len(tag_data) > 0:
                # tag_list = [Tag(article_id=article.id, tagging=d) for d in tag_data]
                tag_list = [{'article_id': article.id, 'tagging': d} for d in tag_data]
                self.tag_handler.create(tags=tag_list)

            # Upload file
            if files is not None and len(files) > 0:
                for f in files:
                    result_flag = await self.attached_file_handler.upload(f=f)
                    if result_flag is True:
                        attached_file = AttachedFile(
                            article_id=article.id,
                            s3_bucket_name=S3_BUCKET['BOARD'],
                            s3_key=f"{S3_KEY_PREFIX['BOARD']}/{f.filename}",
                            filename=f.filename,
                            file_size=f.size,
                            file_type=f.content_type
                        )
                        self.attached_file_handler.create(attached_file=attached_file)
            return True

    async def update_article(self, article_id: int, article_data: ArticleUpsert, tag_data: List[str] = None, files: List[UploadFile] = None ):
        with self.transaction_manager.transaction():
            # Check article
            article = self.article_handler.get_detail(article_id=article_id)
            if article is None:
                raise NotExistArticle()
            # Update article
            self.article_handler.update(article=article, article_data=article_data)

            # Update tags
            if tag_data is not None and len(tag_data) > 0:
                origin_tag_list = sorted([t.tagging for t in article.tags])
                if origin_tag_list is not None and len(origin_tag_list) > 0:
                    if origin_tag_list != sorted(tag_data):
                        # 기존에 입력되어 있던 Tag와 수정 데이터로 받은 tag 리스트가 다른 경우
                        # 기존 Tag 삭제
                        self.tag_handler.delete_all(article_id=article.id)

                # 신규 Tag 입력
                # tags = [Tag(article_id=article.id, tagging=d) for d in tag_data]
                tags = [{'article_id': article_id, 'tagging': d} for d in tag_data]
                self.tag_handler.create(tags=tags)

            # Upload files 처리
            # Upload file은 기존 첨부 파일의 다음 순서로 업로드 순서대로 새로 첨부된다.
            # 기존 첨부되었던 파일의 삭제는 attached_file API의 삭제 API를 호출하여 처리한다.
            if files is not None and len(files) > 0:
                for f in files:
                    result_flag = await self.attached_file_handler.upload(f=f)
                    if result_flag is True:
                        attached_file = AttachedFile(
                            article_id=article.id,
                            s3_bucket_name=S3_BUCKET['BOARD'],
                            s3_key=f"{S3_KEY_PREFIX['BOARD']}/{f.filename}",
                            filename=f.filename,
                            file_size=f.size,
                            file_type=f.content_type
                        )
                        self.attached_file_handler.create(attached_file=attached_file)
            return True

    def delete_article(self, article_id: int):
        with self.transaction_manager.transaction():
            # Check target article
            article = self.article_handler.get_detail(article_id=article_id)
            if article is None:
                raise NotExistArticle()

            # Delete comment for article
            self.comment_handler.delete_all(article_id=article_id)

            # Delete all tags for article
            self.tag_handler.delete_all(article_id=article_id)

            # Delete all attached_file for article
            self.attached_file_handler.delete_all(article_id=article_id)

            # Delete article
            self.article_handler.delete(article=article)

            return True


class CommentService:

    def __init__(self, comment_handler: CommentHandler, article_handler: ArticleHandler, transaction_manager: TransactionManager):
        self.comment_handler = comment_handler
        self.article_handler = article_handler
        self.transaction_manager = transaction_manager

    def get_comment_list(self, article_id: int, page: int, size: int):
        article = self.article_handler.get_detail(article_id=article_id)
        if article is None:
            raise NotExistArticle()
        result_service = self.comment_handler.get_list(article_id=article.id, page=page, size=size)
        return result_service

    def get_comment_detail(self, comment_id: int):
        return self.comment_handler.get_detail(comment_id=comment_id)

    def create_comment(self, comment_create: CommentCreate, article_id: int):
        with self.transaction_manager.transaction():
            article = self.article_handler.get_detail(article_id=article_id)
            if article is None:
                raise NotExistArticle()
            comment_create.article_id = article.id
            self.comment_handler.create(comment_create=comment_create)
            return True

    def update_comment(self, article_id: int, comment_id: int, update_data: CommentCreate):
        with self.transaction_manager.transaction():
            article = self.article_handler.get_detail(article_id=article_id)
            if article is None:
                raise NotExistArticle()
            comment = self.comment_handler.get_detail(comment_id=comment_id)
            if comment is None:
                raise NotExistComment()
            self.comment_handler.update(comment=comment, update_data=update_data)
            return True

    def delete_comment(self, article_id: int, comment_id: int):
        with self.transaction_manager.transaction():
            article = self.article_handler.get_detail(article_id=article_id)
            if article is None:
                raise NotExistArticle()
            comment = self.comment_handler.get_detail(comment_id=comment_id)
            if comment is None:
                raise NotExistComment()
            self.comment_handler.delete(comment=comment)
            return True

    def delete_comment_all(self, article_id: int):
        with self.transaction_manager.transaction():
            self.comment_handler.delete_all(article_id=article_id)
            return True

class TagService:

    def __init__(self, tag_handler: TagHandler, transaction_manager: TransactionManager):
        self.tag_handler = tag_handler
        self.transaction_manager = transaction_manager

    def delete(self, tag_id: int):
        with self.transaction_manager.transaction():
            tag = self.tag_handler.get_detail(tag_id=tag_id)
            if tag is None:
                raise NotExistTag()
            return self.tag_handler.delete(tag=tag)



class AttachedFileService:

    def __init__(self, attached_file_handler: AttachedFileHandler, transaction_manager: TransactionManager):
        self.attached_file_handler = attached_file_handler
        self.transaction_manager = transaction_manager

    def get_attached_file_download(self, attached_file_id: int):
        attached_file = self.attached_file_handler.get_detail(attached_file_id=attached_file_id)
        if attached_file is None:
            raise NotExistAttachedFile()

        contents = self.attached_file_handler.get_content(attached_file=attached_file)
        filename = attached_file.file_name

        return contents, filename
