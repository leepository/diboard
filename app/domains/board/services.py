from typing import cast

from app.domains.board.models import Article
# from app.domains.board.repositories.repository import ArticleRepository
from app.domains.board.handlers import ArticleHandler
from app.domains.board.schemas import ArticleCreate

class ArticleService:

    def __init__(self, article_handler: ArticleHandler):
        self.article_handler = article_handler

    def create_article(self, article: Article):
        return self.article_handler.create(article=article)

    def get_article_list(self, page: int, size: int):
        return self.article_handler.get_list(page=page, size=size)

    def get_article_detail(self, article_id: int):
        return self.article_handler.get_detail(article_id=article_id)
