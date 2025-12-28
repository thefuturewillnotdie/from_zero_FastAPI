from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

PostTag = Table(
    "posts_tags",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("post_id", ForeignKey("posts.id")),
    Column("tag_id", ForeignKey("tags.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    password_hash = Column(String, nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="posts")

    tags = relationship(
        "Tag", secondary=PostTag, back_populates="posts", cascade="all, delete"
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)

    posts = relationship("Post", secondary=PostTag, back_populates="tags")
