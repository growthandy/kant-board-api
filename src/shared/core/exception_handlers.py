from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from shared.core.exceptions import SharedException
from shared.core.logger import get_logger
from shared.core.schemas import APIResponse

logger = get_logger(__name__)

HTTP_ERROR_CODES = {
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
}


def _json(status_code: int, body: APIResponse, headers: dict | None = None) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"), headers=headers)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(SharedException)
    async def shared_exception_handler(request: Request, exc: SharedException):
        logger.warning("업무 예외 [%s] %s (%s %s)", exc.error_code, exc.message, request.method, request.url.path)
        headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
        return _json(exc.status_code, APIResponse.fail(exc.error_code, exc.message, exc.errors), headers)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors: dict[str, list[str]] = {}
        for err in exc.errors():
            field = ".".join(str(p) for p in err["loc"] if p != "body") or "non_field_errors"
            errors.setdefault(field, []).append(err["msg"])
        logger.warning("입력 검증 실패 (%s %s): %s", request.method, request.url.path, errors)
        return _json(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            APIResponse.fail("REQUEST_VALIDATION_ERROR", "요청 입력값 검증에 실패했습니다.", errors),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        code = HTTP_ERROR_CODES.get(exc.status_code, "HTTP_ERROR")
        return _json(exc.status_code, APIResponse.fail(code, str(exc.detail)), getattr(exc, "headers", None))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("처리되지 않은 오류 (%s %s)", request.method, request.url.path)
        return _json(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            APIResponse.fail("INTERNAL_SERVER_ERROR", "서버 내부 오류가 발생했습니다."),
        )
