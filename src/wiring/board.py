from fastapi import FastAPI

from board.application.service import PostService
from board.infrastructure.repositories import SqlAlchemyPostRepository
from board.presentation.dependencies import provide_post_service
from wiring.user import DbSession


def create_post_service(session: DbSession) -> PostService:
    return PostService(SqlAlchemyPostRepository(session))


def wire_board_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[provide_post_service] = create_post_service
