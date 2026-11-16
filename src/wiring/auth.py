from typing import Annotated

from fastapi import Depends, FastAPI

from auth.application.service import AuthService
from auth.domain.service import TokenProvider
from auth.infrastructure.jwt_provider import JWTTokenProvider
from auth.presentation.dependencies import provide_auth_service
from user.domain.repository import UserRepository
from user.domain.user import User
from user.presentation.dependencies import get_current_user, oauth2_scheme
from wiring.user import create_user_repository, password_hasher

token_provider: TokenProvider = JWTTokenProvider()


def create_auth_service(user_repository: Annotated[UserRepository, Depends(create_user_repository)]) -> AuthService:
    return AuthService(user_repository, password_hasher, token_provider)


async def resolve_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(create_auth_service)],
) -> User:
    return await auth_service.authenticate(token)


def wire_auth_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[provide_auth_service] = create_auth_service
    app.dependency_overrides[get_current_user] = resolve_current_user
