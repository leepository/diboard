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
        return self.session.query(Article).order_by(desc(Article.id)).offset(offset).limit(size).all()

    def get_detail(self, article_id: int):
        return self.session.query(Article).filter(Article.id == article_id).first()

    def create(self, article: Article):
        self.session.add(article)
        self.session.flush()  # 새로 생성되는 ID값 생성을 위해 flush
        return article

    def update(self, article: Article):
        self.session.merge(article)
        return article

    def delete(self, article: Article):
        self.session.delete(article)
        return article


class CommentRdbRepository(CommentRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int, page: int, size: int):
        first_comment = aliased(Comment, name='f_comment')
        second_comment = aliased(Comment, name='s_comment')

        # query = (
        #     select(first_comment, second_comment)
        #     .join(
        #         second_comment,
        #         first_comment.id == second_comment.id,
        #         isouter=True
        #     )
        #     .where(first_comment.level == 0 and first_comment.article_id == article_id)
        # )
        # result = self.session.execute(query)
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

    def update(self, comment: Comment):
        self.session.merge(comment)
        return comment

    def delete(self, comment: Comment):
        try:
            comment.is_deleted = True
            comment.deleted_at = datetime.now()
            self.session.merge(comment)

        except Exception as ex:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            print(f'[EX] {class_name}.{method_name} : ', str(ex.args))
            raise ex

    def delete_all(self, article_id: int):
        try:
            query = (
                update(Comment)
                .where(Comment.article_id == article_id)
                .values(
                    is_deleted=True,
                    deleted_at=datetime.now()
                )
            )
            self.session.execute(query)

        except Exception as ex:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            print(f'[EX] {class_name}.{method_name} : ', str(ex.args))
            raise ex

class TagRdbRepository(TagRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int):
        return self.session.query(Tag).filter(Tag.article_id == article_id).all()

    def get_detail(self, tag_id: int):
        return self.session.query(Tag).filter(Tag.id == tag_id).first()

    def create(self, tags: List[dict]):
        exec_flag = False
        try:
            self.session.bulk_insert_mappings(Tag, tags)
            exec_flag = True
        except Exception as ex:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            print(f'[EX] {class_name}.{method_name} : ', str(ex.args))
            raise ex
        return exec_flag

    def delete(self, tag: Tag):
        try:
            self.session.delete(tag)
        except Exception as ex:
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            print(f'[EX] {class_name}.{method_name} : ', str(ex.args))
            raise ex

    def delete_all(self, article_id: int):
        try:
            self.session.query(Tag).filter(Tag.article_id == article_id).delete()
        except Exception as ex:
            print("<<<<<")
            class_name = self.__class__.__name__
            method_name = inspect.currentframe().f_code.co_name
            print(f'[EX] {class_name}.{method_name} : ', str(ex.args))
            raise ex


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
