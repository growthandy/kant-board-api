from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, raw_password: str) -> str:
        """평문 → 단방향 해시 문자열"""

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        """평문이 해시와 일치하는지"""
