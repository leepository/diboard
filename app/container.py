from dependency_injector import containers, providers
from app.databases.cache import get_redis_client
from app.databases.rdb import SessionLocal

from app.domains.board.repositories.rdb.rdb_repository import ArticleRdbRepository
from app.domains.board.handlers import ArticleHandler
from app.domains.board.services import ArticleService

from app.domains.user.repositories.rdb.rdb_repository import UserRdbRepository
from app.domains.user.handlers import UserHandler

from app.domains.auth.repositories.cache.cache_repository import AuthCacheRepository
from app.domains.auth.handlers import AuthHandler

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.domains.board.apis"])

    # Rdb session
    redis_client = providers.Singleton(get_redis_client)
    session = providers.Factory(SessionLocal)

    # Article
    article_repository = providers.Factory(ArticleRdbRepository, session=session)
    article_handler = providers.Factory(ArticleHandler, article_repository=article_repository)
    article_service = providers.Factory(ArticleService, article_handler=article_handler)

    # User
    user_repository = providers.Factory(UserRdbRepository, session=session)
    user_handler = providers.Factory(UserHandler, user_repository=user_repository)

    # Auth
    auth_repository = providers.Factory(AuthCacheRepository, redis_client=redis_client)
    auth_handler = providers.Factory(AuthHandler, auth_repository=auth_repository)
