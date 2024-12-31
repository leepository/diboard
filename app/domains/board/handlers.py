from app.domains.board.repositories.repository import ArticleRepository
from app.domains.board.models import Article
from app.domains.board.schemas import ArticleCreate

class ArticleHandler:

    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository

    def get_list(self, page: int = 1, size: int = 3):
        return self.article_repository.get_list(page=page, size=size)

    def get_detail(self, article_id: int):
        return self.article_repository.get_detail(article_id=article_id)

    def create(self, article: Article):
        return self.article_repository.create(article=article)

    def update(self, article_id: int, requested_article: ArticleCreate):
        article = self.article_repository.get_detail(article_id=article_id)
        if article is None:
            return None
        for key, value in requested_article.model_dump().items():
            setattr(article, key, value)
        return self.article_repository.update(article=article)

    def delete(self, article_id: int):
        article = self.article_repository.get_detail(article_id=article_id)
        if article is None:
            return None
        return self.article_repository.delete(article=article)
