from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.common.constants import AWS_SECRET_NAME
from app.utils.aws_utils import get_aws_secret_value

def _make_rdb_dsn():
    """
    Make DSN for RDB with secrets manager
    :return:
    """
    secret_value = get_aws_secret_value(secret_name=AWS_SECRET_NAME['RDB'])

    return f"mysql+pymysql://{secret_value['USERNAME']}:{secret_value['PASSWORD']}@{secret_value['HOST']}:{secret_value['PORT']}/{secret_value['DBNAME']}"

SQLALCHEMY_DATABASE_URL = _make_rdb_dsn()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
