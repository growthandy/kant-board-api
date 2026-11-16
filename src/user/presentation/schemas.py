import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SignUpRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={"example": {"email": "andy@example.com", "name": "영민", "password": "Passw0rd!"}},
    )

    email: EmailStr = Field(description="로그인 아이디로 쓰는 이메일")
    name: str = Field(min_length=2, max_length=20, description="이름 2~20자")
    password: str = Field(min_length=8, max_length=64, description="8자 이상, 영문·숫자·특수문자 포함")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    name: str
    role: str
    created_at: datetime | None = None
