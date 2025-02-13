from dependency_injector import containers, providers
from app.databases.cache import get_redis_client
from app.databases.rdb import SessionLocal

from app.domains.board.repositories.rdb.rdb_repository import (
    ArticleRdbRepository,
    CommentRdbRepository
)
from app.domains.board.handlers import (
    ArticleHandler,
    CommentHandler
)
from app.domains.board.services import (
    ArticleService,
    CommentService
)

from app.domains.user.repositories.rdb.rdb_repository import UserRdbRepository
from app.domains.user.handlers import UserHandler
from app.domains.user.services import UserService

from app.domains.auth.repositories.cache.cache_repository import AuthCacheRepository
from app.domains.auth.handlers import AuthHandler
from app.domains.auth.services import AuthService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "app.middlewares.token_validator_middleware",
        "app.domains.auth.apis",
        "app.domains.board.apis",
        "app.domains.user.apis"
    ])

    # Rdb session
    redis_client = providers.Singleton(get_redis_client)
    session = providers.Factory(SessionLocal)

    # Article
    article_repository = providers.Factory(ArticleRdbRepository, session=session)
    article_handler = providers.Factory(ArticleHandler, article_repository=article_repository)
    article_service = providers.Factory(ArticleService, article_handler=article_handler)

    # Comment
    comment_repository = providers.Singleton(CommentRdbRepository, session=session)
    comment_handler = providers.Singleton(CommentHandler, comment_repository=comment_repository)
    comment_service = providers.Singleton(CommentService, comment_handler=comment_handler)

    # User
    user_repository = providers.Factory(UserRdbRepository, session=session)
    user_handler = providers.Factory(UserHandler, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_handler=user_handler)

    # Auth
    auth_repository = providers.Factory(AuthCacheRepository, redis_client=redis_client)
    auth_handler = providers.Singleton(AuthHandler, auth_repository=auth_repository)
    auth_service = providers.Factory(AuthService, auth_handler=auth_handler, user_handler=user_handler)

