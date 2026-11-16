from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from board.domain.post import Post
from board.domain.repository import PostRepository
from board.infrastructure.models import PostModel


def to_domain(model: PostModel) -> Post:
    """ORM → 엔티티 (매퍼). author 는 joinedload 로 이미 실려 있어야 한다."""
    return Post(
        id=model.id, title=model.title, content=model.content,
        author_id=model.author_id, author_name=model.author.name,
        created_at=model.created_at, modified_at=model.modified_at, deleted_at=model.deleted_at,
    )


class SqlAlchemyPostRepository(PostRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _alive(self):
        """삭제되지 않은 글 + 작성자 JOIN 을 한 번에 싣는 기본 SELECT."""
        return (
            select(PostModel)
            .options(joinedload(PostModel.author))
            .where(PostModel.deleted_at.is_(None))
        )

    async def find_by_id(self, post_id: int) -> Post | None:
        model = await self.session.scalar(self._alive().where(PostModel.id == post_id))
        return to_domain(model) if model else None

    async def find_page(self, offset: int, limit: int, keyword: str | None) -> tuple[list[Post], int]:
        conditions = [PostModel.deleted_at.is_(None)]
        if keyword:
            conditions.append(or_(PostModel.title.icontains(keyword), PostModel.content.icontains(keyword)))

        total = await self.session.scalar(select(func.count()).select_from(PostModel).where(*conditions))

        stmt = self._alive().where(*conditions).order_by(PostModel.id.desc()).offset(offset).limit(limit)
        models = (await self.session.scalars(stmt)).all()
        return [to_domain(m) for m in models], total or 0

    async def save(self, post: Post) -> Post:
        if post.id is None:
            model = PostModel(title=post.title, content=post.content, author_id=post.author_id)
            self.session.add(model)
            await self.session.flush()
        else:
            model = await self.session.get(PostModel, post.id)
            model.title, model.content, model.deleted_at = post.title, post.content, post.deleted_at
            await self.session.flush()
        await self.session.refresh(model, attribute_names=["created_at", "modified_at", "author"])
        return to_domain(model)
