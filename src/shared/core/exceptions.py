from fastapi import status


class SharedException(Exception):
    """모든 애플리케이션 예외의 부모."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "BAD_REQUEST",
        errors: dict[str, list[str]] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.errors = errors
        super().__init__(message)


class UnauthorizedException(SharedException):
    """401 — '누구인지 모르겠다' (토큰 없음·위조·만료, 로그인 실패)."""

    def __init__(self, message: str = "인증이 필요합니다.", error_code: str = "UNAUTHORIZED"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, error_code)


class ForbiddenException(SharedException):
    """403 — '누구인지는 알지만 이 일은 못 한다' (남의 글 수정 등)."""

    def __init__(self, message: str = "권한이 없습니다.", error_code: str = "FORBIDDEN"):
        super().__init__(message, status.HTTP_403_FORBIDDEN, error_code)


class NotFoundException(SharedException):
    """404 — 대상이 없다 (없는 글, 삭제된 글)."""

    def __init__(self, message: str = "리소스를 찾을 수 없습니다.", error_code: str = "NOT_FOUND"):
        super().__init__(message, status.HTTP_404_NOT_FOUND, error_code)


class ConflictException(SharedException):
    """409 — 이미 있다 (이메일 중복)."""

    def __init__(self, message: str = "이미 존재하는 리소스입니다.", error_code: str = "CONFLICT"):
        super().__init__(message, status.HTTP_409_CONFLICT, error_code)


class ValidationException(SharedException):
    """422 — 형식은 맞는데 업무 규칙(도메인 검증)에 어긋난다 (비밀번호 규칙 등)."""

    def __init__(
        self,
        message: str = "유효성 검사에 실패했습니다.",
        error_code: str = "VALIDATION_ERROR",
        field_errors: dict[str, list[str]] | None = None,
    ):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_CONTENT, error_code, field_errors or {})
