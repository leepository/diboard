from datetime import datetime
from sqlalchemy import select, and_
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
from app.domains.board.schemas import ArticleCreate

class ArticleRdbRepository(ArticleRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, page: int, size: int):
        offset = (page - 1) * size
        return self.session.query(Article).offset(offset).limit(size).all()

    def get_detail(self, article_id: int):
        return self.session.query(Article).filter(Article.id == article_id).first()

    def create(self, article: Article):
        self.session.add(article)
        self.session.commit()
        self.session.refresh(article)
        return article

    def update(self, article: Article):
        self.session.commit()
        self.session.refresh(article)
        return article

    def delete(self, article: Article):
        self.session.delete(article)
        self.session.refresh(article)
        return article


class CommentRdbRepository(CommentRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int, page: int, size: int):
        first_comment = aliased(Comment, name='f_comment')
        second_comment = aliased(Comment, name='s_comment')

        query = (
            select(first_comment, second_comment)
            .join(
                second_comment,
                first_comment.id == second_comment.id,
                isouter=True
            )
            .where(first_comment.level == 0 and first_comment.article_id == article_id)
        )
        return self.session.execute(query).all()

    def get_detail(self, comment_id: int):
        return self.session.query(Comment).filter(Comment.id == comment_id).first()

    def create(self, comment: Comment):
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def update(self, comment: Comment):
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def delete(self, comment: Comment):
        comment.is_deleted = True
        comment.deleted_at = datetime.now()

        self.session.commit()
        self.session.refresh(comment)
        return comment

class TagRdbRepository(TagRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int):
        result = None
        try:
            result = self.session.query(Tag).filter(Tag.article_id == article_id).all()
        except Exception as ex:
            print("[EX] TagRdb Repository.get_list : ", str(ex.args))
        return result

    def create(self, tags: List[Tag]):
        exec_flag = False
        try:
            self.session.bulk_insert_mappings(Tag, tags)
            exec_flag = True
        except Exception as ex:
            print("[EX] TagRdbRepository.create : ", str(ex.args))
            raise ex
        return exec_flag

    def delete(self, tag: Tag):
        exec_flag = False
        try:
            self.session.delete(tag)
            self.session.commit()
        except Exception as ex:
            print("[EX] TagRdbRepository.delete : ", str(ex.args))
        return exec_flag

    def delete_all(self, article_id: int):
        exec_flag = False
        try:
            self.session.query(Tag).filter(Tag.article_id == article_id).delete()
            self.session.commit()
            exec_flag = True
        except Exception as ex:
            print("[EX] TagRdbRepository.delete_all : ", str(ex.args))
        return exec_flag

class AttachedFileRdbRepository(AttachedFileRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_list(self, article_id: int):
        return self.session.query(AttachedFile).filter(and_(
            AttachedFile.article_id == article_id,
            AttachedFile.is_deleted == False
        )).all()

    def create(self, attached_file: AttachedFile):
        self.session.add(attached_file)
        self.session.commit()
        self.session.refresh(attached_file)
        return attached_file

    def delete(self, attached_file: AttachedFile):
        try:
            self.session.delete(attached_file)
            return True
        except Exception as ex:
            raise ex

    def delete_all(self, article_id: int):
        try:
            self.session.query(AttachedFile).filter(AttachedFile.article_id == article_id).delete()
            self.session.commit()
            return True
        except Exception as ex:
            raise ex