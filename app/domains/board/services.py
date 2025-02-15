from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import List

from app.common.constants import S3_BUCKET, S3_KEY_PREFIX
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
    ArticleCreate,
    CommentCreate
)

class ArticleService:

    def __init__(
            self,
            article_handler: ArticleHandler,
            attached_file_handler: AttachedFileHandler,
            tag_handler: TagHandler,
            session: Session):
        self.article_handler = article_handler
        self.attached_file_handler = attached_file_handler
        self.tag_handler = tag_handler
        self.session = session

    def create_article(self, article: Article, tag_data: List[str], files: List[UploadFile]) -> bool:
        exec_result = False
        try:
            # create article
            article = self.article_handler.create(article=article)

            # create tags
            tags = []
            if len(tag_data) > 0:
                tag_list = [Tag(article_id=article.id, tagging=d) for d in tag_data]
                tags = self.tag_handler.create(tags=tag_list)

            # Upload file
            for f in files:
                result_flag = self.attached_file_handler.upload(f=f)
                if result_flag is True:
                    attached_file = AttachedFile(
                        article_id=article.id,
                        s3_bucket_name=S3_BUCKET,
                        s3_key=f"{S3_KEY_PREFIX}/{f.filename}",
                        filename=f.filename,
                        file_size=f.size,
                        file_type=f.content_type
                    )
                    self.attached_file_handler.create(attached_file=attached_file)
            exec_result = True
        except Exception as ex:
            self.session.rollback()

        return exec_result

    def get_article_list(self, page: int, size: int):
        return self.article_handler.get_list(page=page, size=size)

    def get_article_detail(self, article_id: int):
        article = self.article_handler.get_detail(article_id==article_id)
        if article is None:
            raise NotExistArticle()

        tags = self.tag_handler.get_list(article_id=article.id)
        article.tags = tags

        return article

    def update_article(self, article_id: int, article_data: ArticleCreate, tag_data: List[str] ):
        exec_result = False
        try:
            # Check article
            article = self.article_handler.get_detail(article_id=article_id)
            if article is None:
                raise NotExistArticle()
            # Update article
            self.article_handler.update(article=article, article_data=article_data)

            # Update tags
            if len(tag_data) > 0:
                origin_tag_list = sorted([t.tagging for t in article.tags])
                if origin_tag_list != sorted(tag_data):
                    # 기존에 입력되어 있던 Tag와 수정 데이터로 받은 tag 리스트가 다른 경우
                    # 기존 Tag 삭제
                    self.tag_handler.delete_all(article_id=article.id)
                    # 신규 Tag 입력
                    tags = [Tag(article_id=article.id, tagging=d) for d in tag_data]
                    self.tag_handler.create(tags=tags)

            exec_result = True
        except Exception as ex:
            raise ex

        return exec_result

    def delete_article(self, article_id: int):
        exec_flag = False
        try:
            # Check target article
            article = self.article_handler.get_detail(article_id=article_id)
            if article is None:
                raise NotExistArticle()
            # Delete article
            self.article_handler.delete(article=article)

            # Delete all tags for article
            self.tag_handler.delete_all(article_id=article_id)

            exec_flag = True

        except Exception as ex:
            print("[EX] article_service.delete_article : ", str(ex.args))
            self.session.rollback()
            raise ex

        return exec_flag


class CommentService:

    def __init__(self, comment_handler: CommentHandler, article_handler: ArticleHandler):
        self.comment_handler = comment_handler
        self.article_handler = article_handler

    def create_comment(self, comment: Comment, article_id: int):
        article = self.article_handler.get_detail(article_id=article_id)
        if article is None:
            raise NotExistArticle()
        comment.article_id = article.id
        return self.comment_handler.create(comment=comment)

    def get_comment_list(self, article_id: int, page: int, size: int):
        article = self.article_handler.get_detail(article_id=article_id)
        if article is None:
            raise NotExistArticle()
        return self.comment_handler.get_list(article=article, page=page, size=size)

    def get_comment_detail(self, comment_id: int):
        return self.comment_handler.get_detail(comment_id=comment_id)

    def update_comment(self, article_id: int, comment_id: int, update_data: CommentCreate):
        article = self.article_handler.get_detail(article_id=article_id)
        if article is None:
            raise NotExistArticle()
        comment = self.comment_handler.get_detail(comment_id=comment_id)
        if comment is None:
            raise NotExistComment()
        return self.comment_handler.update(comment=comment, update_data=update_data)

    def delete_comment(self, article_id: int, comment_id: int):
        article = self.article_handler.get_detail(article_id=article_id)
        if article is None:
            raise NotExistArticle()
        comment = self.comment_handler.get_detail(comment_id=comment_id)
        if comment is None:
            raise NotExistComment()
        return self.comment_handler.delete(comment=comment)

class TagService:

    def __init__(self, tag_handler: TagHandler):
        self.tag_handler = tag_handler

    def delete(self, tag_id: int):
        tag = self.tag_handler.get_detail(tag_id=tag_id)
        if tag is None:
            raise NotExistTag()
        return self.tag_handler.delete(tag=tag)



class AttachedFileService:

    def __init__(self, attached_file_handler: AttachedFileHandler):
        self.attached_file_handler = attached_file_handler

    def get_attached_file_download(self, attached_file_id: int):
        attached_file = self.attached_file_handler.get_detail(attached_file_id=attached_file_id)
        if attached_file is None:
            raise NotExistAttachedFile()

        contents = self.attached_file_handler.get_content(attached_file=attached_file)
        filename = attached_file.file_name

        return contents, filename
