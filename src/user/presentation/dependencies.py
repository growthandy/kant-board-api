from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from user.application.service import UserService
from user.domain.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def provide_user_service() -> UserService:
    raise NotImplementedError("UserService 가 주입되지 않았습니다. wiring 을 확인하세요.")


# 자리표시자라도 oauth2_scheme 을 받아야 Swagger 에 Authorize 버튼이 생긴다
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Bearer 토큰 → 로그인한 User. 실패하면 401."""
    raise NotImplementedError("get_current_user 가 주입되지 않았습니다. wiring 을 확인하세요.")
