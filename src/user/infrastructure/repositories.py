import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.domain.repository import UserRepository
from user.domain.user import User
from user.infrastructure.models import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, user_id: uuid.UUID) -> User | None:
        model = await self.session.get(UserModel, user_id)
        return model.to_domain() if model else None

    async def find_by_email(self, email: str) -> User | None:
        model = await self.session.scalar(select(UserModel).where(UserModel.email == email))
        return model.to_domain() if model else None

    async def save(self, user: User) -> User:
        model = UserModel(email=user.email, name=user.name, password_hash=user.password_hash, role=user.role)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model.to_domain()
