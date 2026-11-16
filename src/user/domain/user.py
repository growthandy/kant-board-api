import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from shared.core.exceptions import ValidationException
from user.domain.service import PasswordHasher

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")

Role = Literal["USER", "ADMIN"]


@dataclass
class User:
    email: str
    name: str
    password_hash: str
    role: Role = "USER"
    id: uuid.UUID | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        if not (2 <= len(self.name) <= 20):
            raise ValidationException(
                message="이름은 2자 이상 20자 이하여야 합니다.",
                field_errors={"name": ["이름 길이는 2~20자입니다."]},
            )

    @classmethod
    def create(cls, email: str, name: str, raw_password: str, hasher: PasswordHasher) -> "User":
        """회원가입 팩토리 — 평문 규칙 검사 → 해시 → 엔티티."""
        if not PASSWORD_REGEX.match(raw_password):
            raise ValidationException(
                message="비밀번호 규칙을 만족하지 못했습니다.",
                field_errors={"password": ["8자 이상, 영문·숫자·특수문자(@$!%*#?&)를 모두 포함해야 합니다."]},
            )
        return cls(email=email, name=name, password_hash=hasher.hash(raw_password))

    def verify_password(self, raw_password: str, hasher: PasswordHasher) -> bool:
        return hasher.verify(raw_password, self.password_hash)

    @property
    def is_admin(self) -> bool:
        return self.role == "ADMIN"
