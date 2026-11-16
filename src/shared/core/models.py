from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """모든 ORM 모델의 부모. Base.metadata 에 테이블 정의가 모인다."""


class DateTimeBase:
    """created_at · modified_at · deleted_at 을 모든 테이블에 붙이는 믹스인."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


def init_models() -> None:
    """모델 모듈을 import 해서 Base.metadata 에 테이블을 등록한다."""
    import user.infrastructure.models  # noqa: F401  users 테이블
    import board.infrastructure.models  # noqa: F401  posts 테이블
