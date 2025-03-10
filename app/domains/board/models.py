from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import relationship

from app.databases.rdb import Base

class Article(Base):
    __tablename__ = "tb_article"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('tb_user.id'))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime)

    user = relationship('User', back_populates='articles')
    # comments = relationship('Comment', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='article')
    tags = relationship('Tag', back_populates='article', cascade='all, delete-orphan')
    files = relationship('AttachedFile', back_populates='article', cascade='all, delete-orphan')

class Comment(Base):
    __tablename__ = "tb_article_comment"
    __mapper_args__ = {'confirm_deleted_rows': False}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('tb_user.id'))
    article_id = Column(Integer, ForeignKey('tb_article.id'))
    comment_id = Column(Integer)
    content = Column(Text, nullable=False)
    level = Column(Integer, nullable=False, default=0)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime)

    article = relationship('Article', back_populates='comments')
    user = relationship('User', back_populates='comments')

class Tag(Base):
    __tablename__ = "tb_article_tag"
    __mapper_args__ = {'confirm_deleted_rows': False}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('tb_user.id'))
    article_id = Column(Integer, ForeignKey('tb_article.id'))
    tagging = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime)

    article = relationship("Article", back_populates='tags')
    user = relationship('User', back_populates='tags')

class AttachedFile(Base):
    __tablename__ = "tb_article_attached_file"
    __mapper_args__ = {'confirm_deleted_rows': False}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('tb_user.id'))
    article_id = Column(Integer, ForeignKey('tb_article.id'))
    s3_bucket_name = Column(String(255), nullable=False)
    s3_key = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False, default=0)
    file_type = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime, default=datetime.now)


    article = relationship("Article", back_populates='files')
    user = relationship('User', back_populates='files')