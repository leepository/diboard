import inspect

from datetime import datetime
from sqlalchemy import select, and_, desc, update
from sqlalchemy.orm import (
    aliased,
    Session
)
from typing import List

from app.domains.board.models import (
    Article,
    AttachedFile,
    Comment,
    Tag
)
from app.domains.user.models import User
from app.domains.board.repositories.repository import (
    ArticleRepository,
    AttachedFileRepository,
    CommentRepository,
    TagRepository
)
from app.domains.board.schemas import ArticleUpsert
from app.utils.debug_utils import dpp

class ArticleRdbRepository(ArticleRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, page: int, size: int):
        offset = (page - 1) * size
        return self.session.query(Article).filter(Article.is_deleted == False).order_by(desc(Article.id)).offset(offset).limit(size).all()


    def get_detail(self, article_id: int):
        return self.session.query(Article).filter(Article.id == article_id).first()

    def create(self, article: Article):
        self.session.add(article)
        self.session.flush() # 새로 생성되는 ID값 생성을 위해 flush
        return article

    def update(self, article_id: int, update_article: Article):
        update_dict = {}
        if update_article.title is not None and update_article.title != '':
            update_dict.update({'title': update_article.title})
        if update_article.content is not None and update_article.content != '':
            update_dict.update({'content': update_article.content})

        query = (
            update(Article)
            .where(Article.id == article_id)
            .values(**update_dict)
        )
        self.session.execute(query)

    def delete(self, article: Article):
        self.session.delete(article)


class CommentRdbRepository(CommentRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int, page: int, size: int):
        query = self.session.query(Comment) \
            .filter(Comment.article_id == article_id) \
            .filter(Comment.is_deleted == False) \
            .order_by(desc(Comment.article_id), Comment.level)
        return query.all()

    def get_detail(self, comment_id: int):
        return self.session.query(Comment).filter(Comment.id == comment_id).first()

    def create(self, comment: Comment):
        self.session.add(comment)
        self.session.flush()
        return comment

    def update(self, comment_id: int, comment: Comment):
        query = (
            update(Comment)
            .where(Comment.id == comment_id)
            .values(
                content=comment.content,
                updated_at=datetime.now()
            )
        )
        self.session.execute(query)

    def delete(self, comment: Comment):
        query = (
            update(Comment)
            .where(Comment.id == comment.id)
            .values(
                is_deleted=True,
                deleted_at=datetime.now()
            )
        )
        self.session.execute(query)

    def delete_all(self, article_id: int):
        query = (
            update(Comment)
            .where(Comment.article_id == article_id)
            .values(
                is_deleted=True,
                deleted_at=datetime.now()
            )
        )
        self.session.execute(query)

class TagRdbRepository(TagRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int):
        return self.session.query(Tag).filter(Tag.article_id == article_id).all()

    def get_detail(self, tag_id: int):
        return self.session.query(Tag).filter(Tag.id == tag_id).first()

    def create(self, tags: List[dict]):
        self.session.bulk_insert_mappings(Tag, tags)

    def delete(self, tag: Tag):
        self.session.delete(tag)

    def delete_all(self, article_id: int):
        self.session.query(Tag).filter(Tag.article_id == article_id).delete()


class AttachedFileRdbRepository(AttachedFileRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int):
        return self.session.query(AttachedFile).filter(and_(
            AttachedFile.article_id == article_id,
            AttachedFile.is_deleted == False
        )).all()

    def get_detail(self, attached_file_id: int):
        return self.session.query(AttachedFile).filter(AttachedFile.id == attached_file_id).first()

    def create(self, attached_file: AttachedFile):
        self.session.add(attached_file)
        self.session.flush()
        return attached_file

    def delete(self, attached_file: AttachedFile):
        try:
            self.session.delete(attached_file)
        except Exception as ex:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            print(f'[EX] {class_name}.{method_name} : ', str(ex.args))
            raise ex


    def delete_all(self, article_id: int):
        try:
            self.session.query(AttachedFile).filter(AttachedFile.article_id == article_id).delete()
        except Exception as ex:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            print(f'[EX] {class_name}.{method_name} : ', str(ex.args))
            raise ex
