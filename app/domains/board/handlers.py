from fastapi import UploadFile
from typing import List, Optional

from app.common.constants import (
    S3_BUCKET,
    S3_KEY_PREFIX
)
from app.domains.board.repositories.repository import (
    ArticleRepository,
    AttachedFileRepository,
    CommentRepository,
    TagRepository
)
from app.domains.board.models import (
    Article,
    AttachedFile,
    Comment,
    Tag
)
from app.domains.board.schemas import (
    ArticleData,
    ArticleUpsert,
    CommentCreate,
    CommentData
)
from app.utils.aws_utils import s3_upload_file, s3_read_file
from app.utils.debug_utils import dpp

class ArticleHandler:

    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository

    def get_list(self, page: int = 1, size: int = 3):
        article_list = self.article_repository.get_list(page=page, size=size)
        return article_list

    def get_detail(self, article_id: int):
        article = self.article_repository.get_detail(article_id=article_id)
        return article

    def create(self, insert_article: Article):
        return self.article_repository.create(article=insert_article)

    def update(self, article_id: int, update_article: Article):
        self.article_repository.update(article_id=article_id, update_article=update_article)

    def delete(self, article: Article):
        self.article_repository.delete(article=article)


class CommentHandler:

    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def get_list(self, article_id: int, page: int, size: int):
        comment_list = self.comment_repository.get_list(article_id=article_id, page=page, size=size)
        return comment_list

    def get_detail(self, comment_id: int):
        comment = self.comment_repository.get_detail(comment_id=comment_id)
        return comment

    def create(self, insert_comment: Comment):
        return self.comment_repository.create(comment=insert_comment)

    def update(self, comment_id: int, update_comment: Comment):
        self.comment_repository.update(comment_id=comment_id, comment=update_comment)

    def delete(self, comment: Comment):
        return self.comment_repository.delete(comment=comment)

    def delete_all(self, article_id: int):
        return self.comment_repository.delete_all(article_id=article_id)


class TagHandler:

    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def get_list(self, article_id: int):
        return self.tag_repository.get_list(article_id=article_id)

    def get_detail(self, tag_id: int):
        return self.tag_repository.get_detail(tag_id=tag_id)

    def create(self, tags: List[dict]):
        if len(tags) > 0:
            self.tag_repository.create(tags)

    def delete(self, tag: Tag):
        return self.tag_repository.delete(tag)

    def delete_all(self, article_id: int):
        return self.tag_repository.delete_all(article_id=article_id)


class AttachedFileHandler:

    def __init__(self, attached_file_repository: AttachedFileRepository):
        self.attached_file_repository = attached_file_repository

    def get_list(self, article_id: int):
        return self.attached_file_repository.get_list(article_id=article_id)

    def get_detail(self, attached_file_id: int):
        return self.attached_file_repository.get_detail(attached_file_id=attached_file_id)

    def get_content(self, attached_file: AttachedFile):
        attached_file_content = s3_read_file(
            s3_bucket_name=S3_BUCKET,
            s3_key=attached_file.s3_key
        )
        return attached_file_content

    def create(self, attached_file: AttachedFile):
        return self.attached_file_repository.create(attached_file=attached_file)

    def delete(self, attached_file: AttachedFile):
        return self.attached_file_repository.delete(attached_file=attached_file)

    def delete_all(self, article_id: int):
        return self.attached_file_repository.delete_all(article_id=article_id)

    async def upload(self, f: UploadFile):
        s3_key = f"{S3_KEY_PREFIX['BOARD']}/{f.filename}"
        upload_result = await s3_upload_file(
            upload_file_obj=f,
            s3_bucket_name=S3_BUCKET['BOARD'],
            s3_key=s3_key
        )
        return upload_result




