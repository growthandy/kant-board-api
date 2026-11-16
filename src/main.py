from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.presentation.routers.v1.router import router as auth_router
from board.presentation.routers.v1.router import router as post_router
from shared.core.database import close_db, engine
from shared.core.exception_handlers import register_exception_handlers
from shared.core.logger import get_logger
from shared.core.middleware import register_middlewares
from shared.core.models import Base, init_models
from wiring import wire_dependencies

logger = get_logger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("DB 스키마 확인 완료, 서버 준비")
    yield
    await close_db()


tags_metadata = [
    {"name": "Auth", "description": "회원가입 · 로그인(JWT 발급) · 내 정보. 로그인 후 우측 상단 **Authorize** 로 토큰을 등록한다."},
    {"name": "Posts", "description": "게시글 CRUD. 목록·상세는 공개, 작성은 로그인, 수정·삭제는 **작성자 본인 또는 ADMIN**."},
    {"name": "System", "description": "서버 상태 확인"},
]

app = FastAPI(
    title="Board API",
    description=(
        "KANT CH2·CH3 백엔드 평가 과제 — RESTful 게시판 API\n\n"
        "- 모든 응답은 `APIResponse` 봉투(`success`·`code`·`message`·`errors`·`data`)\n"
        "- 인증: `Authorization: Bearer <JWT>` (만료 기본 60분)\n"
        "- 401 = 인증 실패(누구인지 모름) · 403 = 인가 실패(작성자 아님)"
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

register_middlewares(app)
register_exception_handlers(app)
wire_dependencies(app)
app.include_router(auth_router)
app.include_router(post_router)


@app.get("/health", tags=["System"], summary="헬스 체크")
async def health():
    return {"status": "ok"}
