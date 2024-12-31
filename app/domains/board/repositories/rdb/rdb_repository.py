from sqlalchemy.orm import Session

from app.domains.board.models import Article
from app.domains.board.repositories.repository import ArticleRepository
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
