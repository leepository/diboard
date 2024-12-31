import os

from dataclasses import (
    dataclass,
    make_dataclass
)
from dotwiz import DotWiz
from functools import lru_cache

from app.common.constants import AWS_SECRET_NAME
from app.utils.aws_utils import get_aws_secret_value

base_dir = os.path.dirname(os.path.abspath(__file__))

@dataclass
class Config:
    """
    Basic configuration
    """

    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    DEBUG = True
    ALLOW_SITE = ["*"]
    TRUSTED_HOSTS = ["*"]

    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"

@dataclass
class ProductConfig(Config):
    API_ENV = "PRODUCT"
    DEBUG = False
    DB_ECHO = False
    PROJECT_RELOAD: bool = False

@dataclass
class StagingConfig(Config):
    API_ENV = "STAGING"
    DEBUG = True
    DB_ECHO = False
    PROJECT_RELOAD: bool = True

@dataclass
class DevConfig(Config):
    API_ENV = "DEV"
    DEBUG = True
    DB_ECHO = True
    PROJECT_RELOAD: bool = True

@dataclass
class TestConfig(Config):
    API_ENV = "TEST"
    DEBUG = True
    DB_ECHO = True
    PROJECT_RELOAD: bool = True

@lru_cache(maxsize=1)
def get_config(
        ttl_hash,
        api_env: str = "DEV"
):
    """
    Get config
    :param ttl_hash:
    :param api_env:
    :return:
    """
    # From config
    config = dict(
        PRODUCT=ProductConfig,
        STAGING=StagingConfig,
        DEV=DevConfig,
        TEST=TestConfig
    )
    config_obj = config.get(api_env)

    return config_obj

