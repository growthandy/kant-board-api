import math
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from board.application.service import PostService
from board.presentation.dependencies import provide_post_service
from board.presentation.schemas import PostCreateRequest, PostResponse, PostUpdateRequest
from shared.core.docs import COMMON_ERRORS, error_responses
from shared.core.schemas import APIResponse, PageResponse
from user.domain.user import User
from user.presentation.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"], responses=COMMON_ERRORS)

Service = Annotated[PostService, Depends(provide_post_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
PostId = Annotated[int, Path(ge=1, description="게시글 번호")]


@router.get("", response_model=APIResponse[PageResponse[PostResponse]], summary="게시글 목록")
async def list_posts(
    service: Service,
    page: Annotated[int, Query(ge=1, description="페이지 (1부터)")] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="페이지당 개수 (최대 100)")] = 10,
    keyword: Annotated[str | None, Query(max_length=50, description="제목·본문 검색어")] = None,
):
    posts, total = await service.list(page, size, keyword)
    return APIResponse.ok(PageResponse(
        items=[PostResponse.model_validate(p) for p in posts],
        page=page, size=size, total=total, total_pages=math.ceil(total / size),
    ))


@router.post(
    "",
    response_model=APIResponse[PostResponse],
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성 (로그인 필요)",
    responses=error_responses(401),
)
async def create_post(body: PostCreateRequest, service: Service, user: CurrentUser):
    post = await service.create(body.title, body.content, author=user)
    return APIResponse.ok(PostResponse.model_validate(post), "게시글이 등록되었습니다.")


@router.get("/{post_id}", response_model=APIResponse[PostResponse], summary="게시글 상세",
            responses=error_responses(404))
async def get_post(post_id: PostId, service: Service):
    return APIResponse.ok(PostResponse.model_validate(await service.get(post_id)))


@router.patch(
    "/{post_id}",
    response_model=APIResponse[PostResponse],
    summary="게시글 수정 (작성자·관리자)",
    responses=error_responses(401, 403, 404),
)
async def update_post(post_id: PostId, body: PostUpdateRequest, service: Service, user: CurrentUser):
    post = await service.update(post_id, user, body.title, body.content)
    return APIResponse.ok(PostResponse.model_validate(post), "게시글이 수정되었습니다.")


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="게시글 삭제 (작성자·관리자)",
    responses=error_responses(401, 403, 404),
)
async def delete_post(post_id: PostId, service: Service, user: CurrentUser):
    await service.delete(post_id, user)
