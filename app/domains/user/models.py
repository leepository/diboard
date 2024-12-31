from datetime import datetime
from sqlalchemy import(
    DateTime,
    Column,
    Integer,
    String
)

from app.databases.rdb import Base


class User(Base):
    __tablename__ = "tb_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now())
