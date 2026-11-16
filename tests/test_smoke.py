import asyncio
import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
os.environ["JWT_SECRET_KEY"] = "test-" + "x" * 64
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import httpx  # noqa: E402

from main import app  # noqa: E402


async def scenario():
    Path("test.db").unlink(missing_ok=True)
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
            for email in ("a@test.com", "b@test.com"):
                r = await c.post("/api/v1/auth/signup", json={"email": email, "name": "테스터", "password": "Passw0rd!"})
                assert r.status_code == 201, r.text
            r = await c.post("/api/v1/auth/signup", json={"email": "a@test.com", "name": "중복", "password": "Passw0rd!"})
            assert r.status_code == 409 and r.json()["code"] == "EMAIL_ALREADY_EXISTS"
            r = await c.post("/api/v1/auth/signup", json={"email": "c@test.com", "name": "규칙", "password": "password1"})
            assert r.status_code == 422 and "password" in r.json()["errors"]

            async def token(email):
                r = await c.post("/api/v1/auth/login", data={"username": email, "password": "Passw0rd!"})
                assert r.status_code == 200, r.text
                return {"Authorization": f"Bearer {r.json()['access_token']}"}

            a, b = await token("a@test.com"), await token("b@test.com")
            r = await c.post("/api/v1/auth/login", data={"username": "a@test.com", "password": "wrong!1aa"})
            assert r.status_code == 401 and r.json()["code"] == "INVALID_CREDENTIALS"

            r = await c.post("/api/v1/posts", json={"title": "첫 글", "content": "본문"})
            assert r.status_code == 401 and r.json()["success"] is False
            r = await c.post("/api/v1/posts", json={"title": "첫 글", "content": "본문"}, headers=a)
            assert r.status_code == 201, r.text
            post_id = r.json()["data"]["id"]
            assert r.json()["data"]["author_name"] == "테스터"

            r = await c.patch(f"/api/v1/posts/{post_id}", json={"title": "탈취"}, headers=b)
            assert r.status_code == 403 and r.json()["code"] == "NOT_POST_AUTHOR"
            r = await c.patch(f"/api/v1/posts/{post_id}", json={}, headers=a)
            assert r.status_code == 422
            r = await c.patch(f"/api/v1/posts/{post_id}", json={"title": "수정됨"}, headers=a)
            assert r.status_code == 200 and r.json()["data"]["title"] == "수정됨"

            r = await c.get("/api/v1/posts?page=1&size=10&keyword=수정")
            assert r.json()["data"]["total"] == 1
            r = await c.get("/api/v1/posts?size=1000")
            assert r.status_code == 422 and r.json()["code"] == "REQUEST_VALIDATION_ERROR"

            r = await c.delete(f"/api/v1/posts/{post_id}", headers=a)
            assert r.status_code == 204 and r.content == b""
            r = await c.get(f"/api/v1/posts/{post_id}")
            assert r.status_code == 404 and r.json()["code"] == "POST_NOT_FOUND"
            r = await c.get("/api/v1/posts/abc")
            assert r.status_code == 422
    Path("test.db").unlink(missing_ok=True)


def test_smoke():
    asyncio.run(scenario())
