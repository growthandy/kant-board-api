import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class IssuedToken:
    access_token: str
    expires_at: datetime
    expires_in: int


class TokenProvider(ABC):
    @abstractmethod
    def issue(self, user_id: uuid.UUID) -> IssuedToken:
        """사용자 ID 를 담은 액세스 토큰 발급"""

    @abstractmethod
    def decode(self, token: str) -> uuid.UUID:
        """토큰 검증(서명·만료) 후 사용자 ID 반환. 실패하면 UnauthorizedException"""
