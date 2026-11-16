import logging
import os

from dotenv import load_dotenv

load_dotenv()

log_level = logging.DEBUG if os.getenv("LOGGING_MODE", "info").lower() == "debug" else logging.INFO

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)


def get_logger(name: str | None = None) -> logging.Logger:
    """모듈마다 get_logger(__name__) 로 불러 '어느 모듈의 로그인지' 이름을 남긴다."""
    return logging.getLogger(name or "app")
