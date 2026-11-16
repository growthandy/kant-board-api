import uuid

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from shared.core.models import Base, DateTimeBase
from user.domain.user import User


class UserModel(Base, DateTimeBase):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="USER", nullable=False)

    def to_domain(self) -> User:
        """ORM → 엔티티"""
        return User(
            id=self.id, email=self.email, name=self.name,
            password_hash=self.password_hash, role=self.role, created_at=self.created_at,
        )
