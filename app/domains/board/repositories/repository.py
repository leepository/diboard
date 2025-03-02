from abc import ABC, abstractmethod
from typing import List

from app.domains.board.models import (
    Article,
    AttachedFile,
    Comment,
    Tag
)

class ArticleRepository(ABC):

    @abstractmethod
    def get_list(self, page: int, size: int):
        pass

    @abstractmethod
    def get_detail(self, article_id: int):
        pass

    @abstractmethod
    def create(self, article: Article):
        pass

    @abstractmethod
    def update(self, article_id: int, update_article: Article):
        pass

    @abstractmethod
    def delete(self, article: Article):
        pass


class CommentRepository(ABC):

    @abstractmethod
    def get_list(self, article_id: int, page: int, size: int):
        pass

    @abstractmethod
    def get_detail(self, comment_id: int):
        pass

    @abstractmethod
    def create(self, comment: Comment):
        pass

    @abstractmethod
    def update(self, comment: Comment):
        pass

    @abstractmethod
    def delete(self, comment: Comment):
        pass

    @abstractmethod
    def delete_all(self, article_id: int):
        pass


class TagRepository(ABC):

    @abstractmethod
    def get_list(self, article_id: int):
        pass

    @abstractmethod
    def get_detail(self, tag_id: int):
        pass

    @abstractmethod
    def create(self, tags: List[dict]):
        pass

    @abstractmethod
    def delete(self, tag: Tag):
        pass

    @abstractmethod
    def delete_all(self, article_id: int):
        pass


class AttachedFileRepository(ABC):

    @abstractmethod
    def get_list(self, article_id: int):
        pass

    def get_detail(self, attached_file_id: int):
        pass

    @abstractmethod
    def create(self, attached_file: AttachedFile):
        pass

    @abstractmethod
    def delete(self, attached_file: AttachedFile):
        pass

    @abstractmethod
    def delete_all(self, article_id: int):
        pass
