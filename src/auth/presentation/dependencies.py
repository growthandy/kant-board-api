from auth.application.service import AuthService


def provide_auth_service() -> AuthService:
    raise NotImplementedError("AuthService 가 주입되지 않았습니다. wiring 을 확인하세요.")
