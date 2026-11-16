from fastapi import FastAPI

from wiring.auth import wire_auth_dependencies
from wiring.board import wire_board_dependencies
from wiring.user import wire_user_dependencies


def wire_dependencies(app: FastAPI) -> None:
    wire_user_dependencies(app)
    wire_auth_dependencies(app)
    wire_board_dependencies(app)
