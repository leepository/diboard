from typing import List

from app.domains.board.repositories.repository import (
    ArticleRepository,
    CommentRepository,
    TagRepository
)
from app.domains.board.models import (
    Article,
    Comment,
    Tag
)
from app.domains.board.schemas import (
    ArticleCreate,
    CommentCreate
)

class ArticleHandler:

    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository

    def get_list(self, page: int = 1, size: int = 3):
        return self.article_repository.get_list(page=page, size=size)

    def get_detail(self, article_id: int):
        return self.article_repository.get_detail(article_id=article_id)

    def create(self, article: Article):
        return self.article_repository.create(article=article)

    def update(self, article: Article, article_data: ArticleCreate):
        for key, value in article_data.model_dump().items():
            if key not in ["tags"]:
                setattr(article, key, value)
        return self.article_repository.update(article=article)

    def delete(self, article: Article):
        return self.article_repository.delete(article=article)


class CommentHandler:

    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def get_list(self, article: Article, page: int, size: int):
        return self.comment_repository.get_list(article_id=article.id, page=page, size=size)

    def get_detail(self, comment_id: int):
        return self.comment_repository.get_detail(comment_id=comment_id)

    def create(self, comment: Comment):
        return self.comment_repository.create(comment=comment)

    def update(self, comment: Comment, update_data: CommentCreate):
        for key, value in update_data.model_dump().items():
            setattr(comment, key, value)
        return self.comment_repository.update(comment=comment)

    def delete(self, comment: Comment):
        return self.comment_repository.delete(comment=comment)


class TagHandler:

    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository

    def get_list(self, article_id: int):
        return self.tag_repository.get_list(article_id=article_id)

    def create(self, tags: List[Tag]):
        return self.tag_repository.create(tags)

    def delete(self, tag: Tag):
        return self.tag_repository.delete(tag)

    def delete_all(self, article_id: int):
        return self.tag_repository.delete_all(article_id=article_id)
