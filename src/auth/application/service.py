from auth.domain.service import IssuedToken, TokenProvider
from shared.core.exceptions import UnauthorizedException
from user.domain.repository import UserRepository
from user.domain.service import PasswordHasher
from user.domain.user import User


class AuthService:
    def __init__(self, user_repository: UserRepository, hasher: PasswordHasher, token_provider: TokenProvider):
        self.user_repository = user_repository
        self.hasher = hasher
        self.token_provider = token_provider

    async def login(self, email: str, password: str) -> IssuedToken:
        user = await self.user_repository.find_by_email(email)
        if user is None or not user.verify_password(password, self.hasher):
            raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다.", "INVALID_CREDENTIALS")
        return self.token_provider.issue(user.id)

    async def authenticate(self, token: str) -> User:
        """보호 API 마다 호출: 토큰 → 사용자 ID → DB 의 실제 사용자"""
        user_id = self.token_provider.decode(token)
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise UnauthorizedException("존재하지 않는 사용자입니다.", "USER_NOT_FOUND")
        return user
