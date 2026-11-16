from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.application.service import AuthService
from auth.presentation.dependencies import provide_auth_service
from auth.presentation.schemas import TokenResponse
from shared.core.docs import COMMON_ERRORS, error_responses
from shared.core.schemas import APIResponse
from user.application.service import UserService
from user.domain.user import User
from user.presentation.dependencies import get_current_user, provide_user_service
from user.presentation.schemas import SignUpRequest, UserResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"], responses=COMMON_ERRORS)


@router.post(
    "/signup",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    responses=error_responses(409),
)
async def sign_up(
    body: SignUpRequest,
    user_service: Annotated[UserService, Depends(provide_user_service)],
):
    user = await user_service.register(email=body.email, name=body.name, password=body.password)
    return APIResponse.ok(UserResponse.model_validate(user), "회원가입이 완료되었습니다.")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="로그인 (JWT 발급)",
    description="**폼 데이터**로 받는다 (OAuth2 password 규격). `username` 칸에 **이메일**을 넣는다.",
    responses=error_responses(401),
)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(provide_auth_service)],
):
    issued = await auth_service.login(email=form.username, password=form.password)
    return TokenResponse(access_token=issued.access_token, expires_in=issued.expires_in)


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
    summary="내 정보 (토큰 확인용)",
    responses=error_responses(401),
)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return APIResponse.ok(UserResponse.model_validate(current_user))
