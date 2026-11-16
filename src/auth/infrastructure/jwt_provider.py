import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

from auth.domain.service import IssuedToken, TokenProvider
from shared.core.exceptions import UnauthorizedException

load_dotenv()


class JWTTokenProvider(TokenProvider):
    ALGORITHM = "HS512"

    def __init__(self) -> None:
        secret = os.getenv("JWT_SECRET_KEY")
        if not secret:
            raise RuntimeError("JWT_SECRET_KEY 환경변수가 없습니다. .env 를 확인하세요.")
        self.secret_key = secret
        self.expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    def issue(self, user_id: uuid.UUID) -> IssuedToken:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=self.expire_minutes)
        payload = {
            "sub": str(user_id),
            "jti": str(uuid.uuid4()),
            "iat": now,
            "exp": expires_at,
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.ALGORITHM)
        return IssuedToken(token, expires_at, int((expires_at - now).total_seconds()))

    def decode(self, token: str) -> uuid.UUID:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.ALGORITHM],
                options={"require": ["sub", "jti", "iat", "exp"]},
            )
            return uuid.UUID(payload["sub"])
        except (jwt.PyJWTError, ValueError):
            raise UnauthorizedException("유효하지 않거나 만료된 토큰입니다.", "INVALID_TOKEN")
