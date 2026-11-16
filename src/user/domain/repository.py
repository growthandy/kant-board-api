import uuid
from abc import ABC, abstractmethod

from user.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: uuid.UUID) -> User | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> User:
        """신규면 INSERT 후 id 가 채워진 User 를 돌려준다."""
