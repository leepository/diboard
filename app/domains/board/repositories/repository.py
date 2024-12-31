from abc import ABC, abstractmethod

from app.domains.board.models import Article

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
    def update(self, article: Article):
        pass

    @abstractmethod
    def delete(self, article: Article):
        pass
