# 검증 기록 — 실 PostgreSQL 17 (Docker)

- 실행일: 2026-11-16 00:52 UTC · 서버: `uv run uvicorn main:app --app-dir src --port 8077`
- 결과: **0 실패** 

### ✅ 회원가입 A

`POST /api/v1/auth/signup` {"json": {"email": "author-15f3f4@test.com", "name": "작성자", "password": "Passw0rd!"}} → **201** (기대 201)

```json
{
  "success": true,
  "code": "OK",
  "message": "회원가입이 완료되었습니다.",
  "errors": null,
  "data": {
    "id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
    "email": "author-15f3f4@test.com",
    "name": "작성자",
    "role": "USER",
    "created_at": "2026-11-16T00:52:41.674185Z"
  },
  "responded_at": "2026-11-16T00:52:41.911213Z"
}
```

### ✅ 회원가입 B

`POST /api/v1/auth/signup` {"json": {"email": "other-15f3f4@test.com", "name": "다른사람", "password": "Passw0rd!"}} → **201** (기대 201)

```json
{
  "success": true,
  "code": "OK",
  "message": "회원가입이 완료되었습니다.",
  "errors": null,
  "data": {
    "id": "4081b90c-1dbe-4878-a556-02a660127616",
    "email": "other-15f3f4@test.com",
    "name": "다른사람",
    "role": "USER",
    "created_at": "2026-11-16T00:52:41.916213Z"
  },
  "responded_at": "2026-11-16T00:52:42.151729Z"
}
```

### ✅ 중복 가입 → 409

`POST /api/v1/auth/signup` {"json": {"email": "author-15f3f4@test.com", "name": "중복", "password": "Passw0rd!"}} → **409** (기대 409)

```json
{
  "success": false,
  "code": "EMAIL_ALREADY_EXISTS",
  "message": "이미 사용 중인 이메일입니다.",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.158577Z"
}
```

### ✅ 약한 비밀번호 → 422

`POST /api/v1/auth/signup` {"json": {"email": "weak-15f3f4@test.com", "name": "규칙", "password": "password1"}} → **422** (기대 422)

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "비밀번호 규칙을 만족하지 못했습니다.",
  "errors": {
    "password": [
      "8자 이상, 영문·숫자·특수문자(@$!%*#?&)를 모두 포함해야 합니다."
    ]
  },
  "data": null,
  "responded_at": "2026-11-16T00:52:42.162889Z"
}
```

### ✅ 잘못된 이메일 형식 → 422

`POST /api/v1/auth/signup` {"json": {"email": "not-an-email", "name": "x", "password": "Passw0rd!"}} → **422** (기대 422)

```json
{
  "success": false,
  "code": "REQUEST_VALIDATION_ERROR",
  "message": "요청 입력값 검증에 실패했습니다.",
  "errors": {
    "email": [
      "value is not a valid email address: An email address must have an @-sign."
    ],
    "name": [
      "String should have at least 2 characters"
    ]
  },
  "data": null,
  "responded_at": "2026-11-16T00:52:42.164492Z"
}
```

### ✅ 로그인 A (form)

`POST /api/v1/auth/login` {"data": {"username": "author-15f3f4@test.com", "password": "Passw0rd!"}} → **200** (기대 200)

```json
{
  "access_token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4NzEzNzJkNy1hYmY4LTQwZjEtYjA1Yy0xOTM1M2I4Yzg4YzEiLCJqdGkiOiIzZGZjNWU3My1lZWQzLTRhZTctOWFiOC1jYzY2MjFjMDIzMWMiLCJpYXQiOjE3OTQ3OTAzNjIsImV4cCI6MTc5NDc5Mzk2Mn0.97qowXhiOfU7pJ14dtgAZvlgE-VYafWYDU2oeletJvg9EvPTOPfu7gASoUr-wEzWammWxhHqe2y3V75LANrlYA",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### ✅ 로그인 B (form)

`POST /api/v1/auth/login` {"data": {"username": "other-15f3f4@test.com", "password": "Passw0rd!"}} → **200** (기대 200)

```json
{
  "access_token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDgxYjkwYy0xZGJlLTQ4NzgtYTU1Ni0wMmE2NjAxMjc2MTYiLCJqdGkiOiI5N2Q5NzQzNi1jZTZjLTQ3NzMtOWJlMC1lZjQ1ZTI5ZTRiZTIiLCJpYXQiOjE3OTQ3OTAzNjIsImV4cCI6MTc5NDc5Mzk2Mn0.tzcnYCksCWEvOSDRAMlWTyMHgaOhP2Tyuz8OtGWgYLgE8r7pRwaAfCJ29JhZEUu_mQ317PAMtceZi1s-xAlj_Q",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### ✅ 틀린 비밀번호 → 401

`POST /api/v1/auth/login` {"data": {"username": "author-15f3f4@test.com", "password": "Wrong!123"}} → **401** (기대 401)

```json
{
  "success": false,
  "code": "INVALID_CREDENTIALS",
  "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.884597Z"
}
```

### ✅ 내 정보 (토큰)

`GET /api/v1/auth/me` (Bearer)  → **200** (기대 200)

```json
{
  "success": true,
  "code": "OK",
  "message": "요청이 성공적으로 처리되었습니다.",
  "errors": null,
  "data": {
    "id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
    "email": "author-15f3f4@test.com",
    "name": "작성자",
    "role": "USER",
    "created_at": "2026-11-16T00:52:41.674185Z"
  },
  "responded_at": "2026-11-16T00:52:42.890531Z"
}
```

### ✅ /docs (Swagger UI)

`GET /docs`  → **200** (기대 200)

```json
<1008 bytes text/html; charset=utf-8>
```

### ✅ /openapi.json 보안 스킴 (Authorize 버튼)

```json
{
  "OAuth2PasswordBearer": {
    "type": "oauth2",
    "flows": {
      "password": {
        "scopes": {},
        "tokenUrl": "/api/v1/auth/login"
      }
    }
  }
}
```

### ✅ 토큰 없이 글쓰기 → 401

`POST /api/v1/posts` {"json": {"title": "t", "content": "c"}} → **401** (기대 401)

```json
{
  "success": false,
  "code": "UNAUTHORIZED",
  "message": "Not authenticated",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.910449Z"
}
```

### ✅ 엉터리 토큰 → 401

`POST /api/v1/posts` (Bearer) {"json": {"title": "t", "content": "c"}} → **401** (기대 401)

```json
{
  "success": false,
  "code": "INVALID_TOKEN",
  "message": "유효하지 않거나 만료된 토큰입니다.",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.912077Z"
}
```

### ✅ 만료 토큰 → 401

`POST /api/v1/posts` (Bearer) {"json": {"title": "t", "content": "c"}} → **401** (기대 401)

```json
{
  "success": false,
  "code": "INVALID_TOKEN",
  "message": "유효하지 않거나 만료된 토큰입니다.",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.913885Z"
}
```

### ✅ 빈 제목 → 422 (공통 봉투)

`POST /api/v1/posts` (Bearer) {"json": {"title": "", "content": "c"}} → **422** (기대 422)

```json
{
  "success": false,
  "code": "REQUEST_VALIDATION_ERROR",
  "message": "요청 입력값 검증에 실패했습니다.",
  "errors": {
    "title": [
      "String should have at least 1 character"
    ]
  },
  "data": null,
  "responded_at": "2026-11-16T00:52:42.919305Z"
}
```

### ✅ 글 작성 1

`POST /api/v1/posts` (Bearer) {"json": {"title": "[15f3f4] 글 1", "content": "본문 1"}} → **201** (기대 201)

```json
{
  "success": true,
  "code": "OK",
  "message": "게시글이 등록되었습니다.",
  "errors": null,
  "data": {
    "id": 1,
    "title": "[15f3f4] 글 1",
    "content": "본문 1",
    "author_id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
    "author_name": "작성자",
    "created_at": "2026-11-16T00:52:42.925825Z",
    "modified_at": null
  },
  "responded_at": "2026-11-16T00:52:42.933772Z"
}
```

### ✅ 글 작성 2

`POST /api/v1/posts` (Bearer) {"json": {"title": "[15f3f4] 글 2", "content": "본문 2"}} → **201** (기대 201)

```json
{
  "success": true,
  "code": "OK",
  "message": "게시글이 등록되었습니다.",
  "errors": null,
  "data": {
    "id": 2,
    "title": "[15f3f4] 글 2",
    "content": "본문 2",
    "author_id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
    "author_name": "작성자",
    "created_at": "2026-11-16T00:52:42.936984Z",
    "modified_at": null
  },
  "responded_at": "2026-11-16T00:52:42.941846Z"
}
```

### ✅ 글 작성 3

`POST /api/v1/posts` (Bearer) {"json": {"title": "[15f3f4] 글 3", "content": "본문 3"}} → **201** (기대 201)

```json
{
  "success": true,
  "code": "OK",
  "message": "게시글이 등록되었습니다.",
  "errors": null,
  "data": {
    "id": 3,
    "title": "[15f3f4] 글 3",
    "content": "본문 3",
    "author_id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
    "author_name": "작성자",
    "created_at": "2026-11-16T00:52:42.944137Z",
    "modified_at": null
  },
  "responded_at": "2026-11-16T00:52:42.947156Z"
}
```

### ✅ 목록 페이지네이션 (size=2)

`GET /api/v1/posts` {"params": {"page": 1, "size": 2, "keyword": "15f3f4"}} → **200** (기대 200)

```json
{
  "success": true,
  "code": "OK",
  "message": "요청이 성공적으로 처리되었습니다.",
  "errors": null,
  "data": {
    "items": [
      {
        "id": 3,
        "title": "[15f3f4] 글 3",
        "content": "본문 3",
        "author_id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
        "author_name": "작성자",
        "created_at": "2026-11-16T00:52:42.944137Z",
        "modified_at": null
      },
      {
        "id": 2,
        "title": "[15f3f4] 글 2",
        "content": "본문 2",
        "author_id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
        "author_name": "작성자",
        "created_at": "2026-11-16T00:52:42.936984Z",
        "modified_at": null
      }
    ],
    "page": 1,
    "size": 2,
    "total": 3,
    "total_pages": 2
  },
  "responded_at": "2026-11-16T00:52:42.954089Z"
}
```

### ✅ size 범위 초과 → 422

`GET /api/v1/posts` {"params": {"size": 1000}} → **422** (기대 422)

```json
{
  "success": false,
  "code": "REQUEST_VALIDATION_ERROR",
  "message": "요청 입력값 검증에 실패했습니다.",
  "errors": {
    "query.size": [
      "Input should be less than or equal to 100"
    ]
  },
  "data": null,
  "responded_at": "2026-11-16T00:52:42.955732Z"
}
```

### ✅ 상세 조회

`GET /api/v1/posts/1`  → **200** (기대 200)

```json
{
  "success": true,
  "code": "OK",
  "message": "요청이 성공적으로 처리되었습니다.",
  "errors": null,
  "data": {
    "id": 1,
    "title": "[15f3f4] 글 1",
    "content": "본문 1",
    "author_id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
    "author_name": "작성자",
    "created_at": "2026-11-16T00:52:42.925825Z",
    "modified_at": null
  },
  "responded_at": "2026-11-16T00:52:42.959488Z"
}
```

### ✅ 작성자 수정 → 200

`PATCH /api/v1/posts/1` (Bearer) {"json": {"title": "[15f3f4] 수정됨"}} → **200** (기대 200)

```json
{
  "success": true,
  "code": "OK",
  "message": "게시글이 수정되었습니다.",
  "errors": null,
  "data": {
    "id": 1,
    "title": "[15f3f4] 수정됨",
    "content": "본문 1",
    "author_id": "871372d7-abf8-40f1-b05c-19353b8c88c1",
    "author_name": "작성자",
    "created_at": "2026-11-16T00:52:42.925825Z",
    "modified_at": "2026-11-16T00:52:42.960928Z"
  },
  "responded_at": "2026-11-16T00:52:42.965598Z"
}
```

### ✅ 남이 수정 → 403

`PATCH /api/v1/posts/1` (Bearer) {"json": {"title": "탈취"}} → **403** (기대 403)

```json
{
  "success": false,
  "code": "NOT_POST_AUTHOR",
  "message": "작성자 본인만 수정·삭제할 수 있습니다.",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.969658Z"
}
```

### ✅ 남이 삭제 → 403

`DELETE /api/v1/posts/1` (Bearer)  → **403** (기대 403)

```json
{
  "success": false,
  "code": "NOT_POST_AUTHOR",
  "message": "작성자 본인만 수정·삭제할 수 있습니다.",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.973411Z"
}
```

### ✅ 작성자 삭제 → 204

`DELETE /api/v1/posts/1` (Bearer)  → **204** (기대 204)

```json
<0 bytes >
```

### ✅ 삭제 후 조회 → 404

`GET /api/v1/posts/1`  → **404** (기대 404)

```json
{
  "success": false,
  "code": "POST_NOT_FOUND",
  "message": "게시글을 찾을 수 없습니다.",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.981529Z"
}
```

### ✅ 잘못된 경로 파라미터 → 422

`GET /api/v1/posts/abc`  → **422** (기대 422)

```json
{
  "success": false,
  "code": "REQUEST_VALIDATION_ERROR",
  "message": "요청 입력값 검증에 실패했습니다.",
  "errors": {
    "path.post_id": [
      "Input should be a valid integer, unable to parse string as an integer"
    ]
  },
  "data": null,
  "responded_at": "2026-11-16T00:52:42.982492Z"
}
```

### ✅ 없는 경로 → 404

`GET /api/v1/nope`  → **404** (기대 404)

```json
{
  "success": false,
  "code": "NOT_FOUND",
  "message": "Not Found",
  "errors": null,
  "data": null,
  "responded_at": "2026-11-16T00:52:42.983088Z"
}
```

### ✅ DB 에 bcrypt 해시로 저장 (psql)

```text
$ select email, left(password_hash,7)||'…'||length(password_hash) from users
author-15f3f4@test.com|$2b$12$…60
other-15f3f4@test.com|$2b$12$…60
```

### posts 테이블 (FK 확인)

```text
                                       Table "public.posts"
   Column    |           Type           | Collation | Nullable |              Default              
-------------+--------------------------+-----------+----------+-----------------------------------
 id          | bigint                   |           | not null | nextval('posts_id_seq'::regclass)
 title       | character varying(100)   |           | not null | 
 content     | text                     |           | not null | 
 author_id   | uuid                     |           | not null | 
 created_at  | timestamp with time zone |           | not null | now()
 modified_at | timestamp with time zone |           |          | 
 deleted_at  | timestamp with time zone |           |          | 
Indexes:
    "posts_pkey" PRIMARY KEY, btree (id)
    "ix_posts_author_id" btree (author_id)
    "ix_posts_deleted_at_id" btree (deleted_at, id)
Foreign-key constraints:
    "posts_author_id_fkey" FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE

```
