import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from shared.core.exceptions import ForbiddenException, ValidationException
from user.domain.user import User


@dataclass
class Post:
    title: str
    content: str
    author_id: uuid.UUID
    author_name: str | None = None
    id: int | None = None
    created_at: datetime | None = None
    modified_at: datetime | None = None
    deleted_at: datetime | None = None

    def __post_init__(self):
        self._validate(self.title, self.content)

    @staticmethod
    def _validate(title: str, content: str) -> None:
        errors: dict[str, list[str]] = {}
        if not title.strip() or len(title) > 100:
            errors["title"] = ["제목은 공백이 아닌 1~100자여야 합니다."]
        if not content.strip() or len(content) > 5000:
            errors["content"] = ["본문은 공백이 아닌 1~5000자여야 합니다."]
        if errors:
            raise ValidationException("게시글 유효성 검사에 실패했습니다.", field_errors=errors)

    @classmethod
    def create(cls, title: str, content: str, author: User) -> "Post":
        return cls(title=title.strip(), content=content.strip(), author_id=author.id, author_name=author.name)

    def ensure_editable_by(self, requester: User) -> None:
        """작성자 검증 — 인가(authorization)의 핵심."""
        if not (requester.is_admin or self.author_id == requester.id):
            raise ForbiddenException("작성자 본인만 수정·삭제할 수 있습니다.", "NOT_POST_AUTHOR")

    def update(self, title: str | None, content: str | None) -> None:
        """PATCH = 부분 수정. 보낸 칸만 바꾼다 (None = 안 보냄)."""
        new_title = title.strip() if title is not None else self.title
        new_content = content.strip() if content is not None else self.content
        self._validate(new_title, new_content)
        self.title, self.content = new_title, new_content

    def delete(self) -> None:
        self.deleted_at = datetime.now(timezone.utc)
