from board.domain.post import Post
from board.domain.repository import PostRepository
from shared.core.exceptions import NotFoundException
from user.domain.user import User


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def create(self, title: str, content: str, author: User) -> Post:
        return await self.repository.save(Post.create(title, content, author))

    async def get(self, post_id: int) -> Post:
        post = await self.repository.find_by_id(post_id)
        if post is None:
            raise NotFoundException("게시글을 찾을 수 없습니다.", "POST_NOT_FOUND")
        return post

    async def list(self, page: int, size: int, keyword: str | None) -> tuple[list[Post], int]:
        return await self.repository.find_page(offset=(page - 1) * size, limit=size, keyword=keyword)

    async def update(self, post_id: int, requester: User, title: str | None, content: str | None) -> Post:
        post = await self.get(post_id)
        post.ensure_editable_by(requester)
        post.update(title, content)
        return await self.repository.save(post)

    async def delete(self, post_id: int, requester: User) -> None:
        post = await self.get(post_id)
        post.ensure_editable_by(requester)
        post.delete()
        await self.repository.save(post)
