import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PostCreateRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={"example": {"title": "첫 글", "content": "FastAPI 게시판 테스트입니다."}},
    )
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=5000)


class PostUpdateRequest(BaseModel):
    """PATCH 바디 — 모든 칸이 선택. 보낸 칸만 바뀐다."""

    model_config = ConfigDict(str_strip_whitespace=True, json_schema_extra={"example": {"title": "제목만 수정"}})
    title: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = Field(None, min_length=1, max_length=5000)

    @model_validator(mode="after")
    def at_least_one(self):
        if self.title is None and self.content is None:
            raise ValueError("title 또는 content 중 하나는 보내야 합니다.")
        return self


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author_id: uuid.UUID
    author_name: str | None
    created_at: datetime | None
    modified_at: datetime | None
