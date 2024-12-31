from dependency_injector import containers, providers
from app.databases.rdb import SessionLocal
from app.domains.board.repositories.rdb.rdb_repository import ArticleRdbRepository
from app.domains.board.handlers import ArticleHandler
from app.domains.board.services import ArticleService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.domains.board.apis"])

    # Rdb session
    session = providers.Factory(SessionLocal)

    # Article
    article_repository = providers.Factory(ArticleRdbRepository, session=session)
    article_handler = providers.Factory(ArticleHandler, article_repository=article_repository)
    article_service = providers.Factory(ArticleService, article_handler=article_handler)
