from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(description="JWT 액세스 토큰")
    token_type: str = Field("bearer", description="항상 bearer")
    expires_in: int = Field(description="만료까지 남은 초")
