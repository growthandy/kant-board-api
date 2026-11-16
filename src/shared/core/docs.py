from typing import Any

from shared.core.schemas import APIResponse

_DESCRIPTIONS = {
    401: "인증 실패 — 토큰 없음·위조·만료, 또는 로그인 정보 불일치",
    403: "권한 없음 — 로그인은 했지만 작성자가 아님",
    404: "대상 없음",
    409: "중복 — 이미 가입된 이메일",
    422: "입력값 검증 실패 — errors 에 필드별 메시지",
}


def error_responses(*codes: int) -> dict[int | str, dict[str, Any]]:
    return {c: {"model": APIResponse[None], "description": _DESCRIPTIONS[c]} for c in codes}


COMMON_ERRORS = error_responses(422)
