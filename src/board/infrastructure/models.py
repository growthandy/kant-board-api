import uuid

from sqlalchemy import BigInteger, ForeignKey, Index, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.core.models import Base, DateTimeBase
from user.infrastructure.models import UserModel


class PostModel(Base, DateTimeBase):
    __tablename__ = "posts"
    __table_args__ = (
        Index("ix_posts_deleted_at_id", "deleted_at", "id"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer(), "sqlite"), primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    author: Mapped[UserModel] = relationship(lazy="raise")
