# EC2 배포 검증 (curl, 2026-11-18)

대상: `http://54.116.87.84` — 내 맥에서 배포 서버로 직접 요청한 기록. 토큰 값은 가렸다.

```text
$ curl -s -o /dev/null -w '%{http_code}' http://54.116.87.84/health
200
$ curl -s -o /dev/null -w '%{http_code}' http://54.116.87.84/docs
200
$ curl -s -o /dev/null -w '%{http_code}' http://54.116.87.84/openapi.json
200

$ curl -sI http://54.116.87.84/health | grep -i server
Server: nginx/1.28.3 (Ubuntu)

$ curl -s -X POST http://54.116.87.84/api/v1/auth/login -d 'username=ec2-demo-a-854561@example.com&password=***'
{"access_token": "eyJhbGciOiJI…(생략)", "token_type": "bearer", "expires_in": 3600}

$ curl -s http://54.116.87.84/api/v1/auth/me -H 'Authorization: Bearer <token>'
{"success":true,"code":"OK","message":"요청이 성공적으로 처리되었습니다.","errors":null,"data":{"id":"777deba5-ce0e-428e-85b5-e314b1f752c7","email":"ec2-demo-a-854561@example.com","name":"데모A","role":"USER","created_at":"2026-11-18T08:01:03.292441Z"},"responded_at":"2026-11-18T08:02:02.938659Z"}

$ curl -s 'http://54.116.87.84/api/v1/posts?page=1&size=2'
{"success":true,"code":"OK","message":"요청이 성공적으로 처리되었습니다.","errors":null,"data":{"items":[{"id":3,"title":"EC2 배포 확인","content":"AWS EC2 + Nginx + systemd 위에서 동작하는 게시판 API 입니다.","author_id":"777deba5-ce0e-428e-85b5-e314b1f752c7","author_name":"데모A","created_at":"2026-11-18T08:01:13.745953Z","modified_at":null},{"id":2,"title":"EC2 배포 확인","content":"AWS EC2 + Nginx + systemd 위에서 동작하는 게시판 API 입니다.","author_id":"5f580c35-8e8b-477c-8a0a-4549d05db74e","author_name":"데모A","created_at":"2026-11-18T08:00:12.898839Z","modified_at":null}],"page":1,"size":2,"total":3,"total_pages":2},"responded_at":"2026-11-18T08:02:03.696710Z"}

$ curl -s -X PATCH http://54.116.87.84/api/v1/posts/3 -H 'Content-Type: application/json' -d '{"title":"토큰 없이"}'   # 401
{"success":false,"code":"UNAUTHORIZED","message":"Not authenticated","errors":null,"data":null,"responded_at":"2026-11-18T08:02:04.575491Z"}
```
