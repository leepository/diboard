import datetime

from sqlalchemy import (
    DateTime,
    Column,
    Integer,
    String
)
from app.databases.rdb import Base

class Article(Base):
    __tablename__ = "tb_article"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
