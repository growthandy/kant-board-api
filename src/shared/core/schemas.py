from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(description="처리 성공 여부")
    code: str = Field(description="성공 시 OK, 실패 시 에러 코드")
    message: str | None = Field(None, description="사람이 읽는 설명")
    errors: dict[str, list[str]] | Any | None = Field(None, description="실패 시 필드별 상세")
    data: T | None = Field(None, description="성공 시 응답 데이터")
    responded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="응답 시각(UTC)",
    )

    @classmethod
    def ok(cls, data: T | None = None, message: str = "요청이 성공적으로 처리되었습니다.") -> "APIResponse[T]":
        return cls(success=True, code="OK", message=message, data=data)

    @classmethod
    def fail(cls, code: str, message: str, errors: Any = None) -> "APIResponse[None]":
        return cls(success=False, code=code, message=message, errors=errors)


class PageResponse(BaseModel, Generic[T]):
    """목록 응답. items 만 주면 클라이언트가 '다음 페이지가 있는지' 를 모른다 → total 을 같이 준다."""

    items: list[T]
    page: int = Field(description="현재 페이지 (1부터)")
    size: int = Field(description="페이지당 개수")
    total: int = Field(description="전체 개수")
    total_pages: int = Field(description="전체 페이지 수")
