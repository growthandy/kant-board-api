from board.application.service import PostService


def provide_post_service() -> PostService:
    raise NotImplementedError("PostService 가 주입되지 않았습니다. wiring 을 확인하세요.")
