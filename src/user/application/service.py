from shared.core.exceptions import ConflictException
from user.domain.repository import UserRepository
from user.domain.service import PasswordHasher
from user.domain.user import User


class UserService:
    def __init__(self, repository: UserRepository, hasher: PasswordHasher):
        self.repository = repository
        self.hasher = hasher

    async def register(self, email: str, name: str, password: str) -> User:
        if await self.repository.find_by_email(email):
            raise ConflictException("이미 사용 중인 이메일입니다.", "EMAIL_ALREADY_EXISTS")
        user = User.create(email=email, name=name, raw_password=password, hasher=self.hasher)
        return await self.repository.save(user)
