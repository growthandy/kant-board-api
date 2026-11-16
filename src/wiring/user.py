from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from shared.core.database import get_db
from user.application.service import UserService
from user.domain.repository import UserRepository
from user.domain.service import PasswordHasher
from user.infrastructure.repositories import SqlAlchemyUserRepository
from user.infrastructure.security import BcryptPasswordHasher
from user.presentation.dependencies import provide_user_service

password_hasher: PasswordHasher = BcryptPasswordHasher()

DbSession = Annotated[AsyncSession, Depends(get_db, scope="function")]


def create_user_repository(session: DbSession) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def create_user_service(repository: Annotated[UserRepository, Depends(create_user_repository)]) -> UserService:
    return UserService(repository=repository, hasher=password_hasher)


def wire_user_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[provide_user_service] = create_user_service
