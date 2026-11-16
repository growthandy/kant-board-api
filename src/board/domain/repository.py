from abc import ABC, abstractmethod

from board.domain.post import Post


class PostRepository(ABC):
    @abstractmethod
    async def find_by_id(self, post_id: int) -> Post | None:
        """삭제되지 않은 글 1건 (작성자 이름 포함)"""

    @abstractmethod
    async def find_page(self, offset: int, limit: int, keyword: str | None) -> tuple[list[Post], int]:
        """최신순 목록 + 전체 개수"""

    @abstractmethod
    async def save(self, post: Post) -> Post:
        """id 가 없으면 INSERT, 있으면 UPDATE (소프트 삭제 포함)"""
