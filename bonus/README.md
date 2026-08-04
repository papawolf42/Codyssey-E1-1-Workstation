# Codyssey E1-1 Workstation — 보너스 체크리스트

## 목표

- [x] Flask, MySQL, Redis 세 컨테이너 사용
- [x] MySQL에 사용자 ID와 비밀번호 해시 저장
- [x] Redis에 접속 시각과 TTL 10초 세션 저장
- [x] 10초 동안 이용하지 않으면 재로그인 안내

## 1) 파일 준비

- [x] `compose.yaml`
- [x] `app.py`
- [x] `Dockerfile`
- [x] `requirements.txt`

## 2) 보너스 1 — 단일 서비스

- [x] MySQL만 실행 — `docker compose up -d mysql`
- [x] 상태 확인 — `docker compose ps`
- [x] 단일 서비스 종료 — `docker compose down`

## 3) 보너스 2 — 멀티 컨테이너

- [x] Flask, MySQL, Redis 실행 — `docker compose up -d --build`
- [x] 세 컨테이너 상태 확인 — `docker compose ps`
- [x] Flask가 서비스 이름 `mysql`로 MySQL에 연결
- [x] Flask가 서비스 이름 `redis`로 Redis에 연결
- [x] Flask 포트만 호스트에 공개
- [x] MySQL과 Redis 포트는 호스트에 공개하지 않음

## 4) 로그인 세션

- [x] MySQL에 테스트 사용자 ID 저장
- [x] 비밀번호 원문 대신 해시 저장
- [x] 로그인 시 ID와 비밀번호 확인
- [x] 로그인 성공 시 Redis 세션 생성
- [x] Redis에 사용자 ID와 접속 시각 저장
- [x] 세션 TTL을 10초로 설정
- [x] 로그인 상태에서 요청하면 TTL을 다시 10초로 갱신
- [x] 10초 동안 요청하지 않으면 세션 자동 삭제
- [x] `세션이 만료되었습니다. 다시 로그인하세요.` 표시
- [x] 재로그인 성공 확인

## 5) 보너스 3 — 운영 명령

- [x] 실행 — `docker compose up -d`
- [x] 상태 — `docker compose ps`
- [x] 로그 — `docker compose logs`
- [x] 종료 — `docker compose down`
- [x] Compose 운영 명령과 실행 결과를 README에 기록

## 6) 보너스 4 — 환경변수

- [x] Dockerfile에서 `APP_MODE=normal`을 앱에 주입
- [x] 응답에서 `mode=normal` 확인
- [x] Compose에서 `APP_MODE=maintenance`로 변경
- [x] 코드 수정 없이 점검 안내와 `mode=maintenance`가 표시되는지 확인

## 7) 최종 확인

- [x] 실제 명령과 출력이 README에 있음
- [x] 비밀번호 원문과 세션 Token을 출력하지 않음
- [x] `docker compose down`으로 실습 컨테이너 정리

## 수행 기록

### MySQL 단일 서비스 실행

```console
$ docker compose up -d mysql
[+] Running 3/3
 ✔ Network my-first-compose_default    Created
 ✔ Volume my-first-compose_mysql-data  Created
 ✔ Container my-first-compose-mysql-1  Started

$ docker compose ps
NAME                       IMAGE       SERVICE   STATUS          PORTS
my-first-compose-mysql-1   mysql:8.4   mysql     Up 59 seconds   3306/tcp, 33060/tcp
```

MySQL 이미지와 컨테이너 하나를 Compose로 실행했다. `3306/tcp`는 컨테이너 내부 포트만 표시되고 호스트 포트 매핑은 없으므로 MySQL을 외부에 공개하지 않은 상태다.

### MySQL 접속 확인

```console
$ docker compose exec mysql mysql -uapp_user -p login_db
Enter password:
Welcome to the MySQL monitor.
Server version: 8.4.11 MySQL Community Server - GPL

mysql> SELECT DATABASE(), CURRENT_USER();
+------------+----------------+
| DATABASE() | CURRENT_USER() |
+------------+----------------+
| login_db   | app_user@%     |
+------------+----------------+
1 row in set (0.00 sec)

mysql> SHOW TABLES;
Empty set (0.01 sec)
```

`app_user` 계정으로 `login_db` 접속에 성공했다. 현재는 데이터베이스만 생성됐으며 사용자 정보를 저장할 테이블은 아직 만들지 않은 상태다.

### Redis 실행 및 연결 확인

```console
$ docker compose up -d redis
[+] Running 8/8
 ✔ redis Pulled
[+] Running 1/1
 ✔ Container my-first-compose-redis-1  Started

$ docker compose ps
NAME                       IMAGE            SERVICE   STATUS       PORTS
my-first-compose-mysql-1   mysql:8.4        mysql     Up 4 hours   3306/tcp, 33060/tcp
my-first-compose-redis-1   redis:7-alpine   redis     Up 2 hours   6379/tcp
```

MySQL과 Redis가 같은 Compose 프로젝트에서 실행됐다. 두 서비스 모두 호스트 포트 매핑이 없으므로 Compose 내부 네트워크에서만 접근할 수 있다.

처음에는 서비스 이름을 일반 Docker 명령에 사용해 오류가 발생했다.

```console
$ docker exec redis redis-cli PING
Error response from daemon: No such container: redis
```

`docker exec`에는 실제 컨테이너 이름인 `my-first-compose-redis-1`이 필요하다. Compose 명령에서는 서비스 이름 `redis`를 사용할 수 있다.

```console
$ docker compose exec redis redis-cli PING
PONG
```

Redis의 `PING` 명령에 `PONG`이 반환되어 Redis 서버가 명령을 처리할 수 있음을 확인했다.

### Redis TTL 10초 확인

```console
$ docker compose exec redis redis-cli SET session:test app_user EX 10
OK

$ docker compose exec redis redis-cli TTL session:test
(integer) 1

$ docker compose exec redis redis-cli TTL session:test
(integer) -2

$ docker compose exec redis redis-cli GET session:test
(nil)
```

`SET session:test app_user EX 10`은 다음과 같이 읽는다.

- `SET`: Redis에 Key와 Value를 저장하는 명령어
- `session:test`: 저장할 Key. `session`은 로그인 세션 용도이고 `test`는 실습용 이름이다. 콜론(`:`)은 관련 단어를 구분하기 위한 관례이며 특별한 연산자는 아니다.
- `app_user`: Key에 저장할 Value. 여기서는 로그인한 사용자 이름을 뜻한다.
- `EX`: 만료 시간을 초 단위로 설정하는 옵션
- `10`: 10초 뒤 해당 Key를 자동으로 삭제한다는 뜻

따라서 이 명령은 `session:test`라는 Key에 `app_user`를 저장하고 TTL(Time To Live)을 10초로 설정한다. 첫 번째 `TTL` 결과 `1`은 만료까지 약 1초가 남았다는 뜻이다. 이후 결과 `-2`와 `GET` 결과 `(nil)`은 10초가 지나 Key가 자동으로 삭제됐다는 뜻이다.

### 세 컨테이너 실행 확인

```console
$ docker compose ps
NAME                       IMAGE                  COMMAND                  SERVICE   STATUS              PORTS
my-first-compose-app-1     my-first-compose-app   "python app.py"          app       Up About a minute   0.0.0.0:5001->5000/tcp, [::]:5001->5000/tcp
my-first-compose-mysql-1   mysql:8.4              "docker-entrypoint.s…"   mysql     Up 6 hours          3306/tcp, 33060/tcp
my-first-compose-redis-1   redis:7-alpine         "docker-entrypoint.s…"   redis     Up 5 hours          6379/tcp
```

Flask, MySQL, Redis가 함께 실행됐다. Flask만 호스트의 `5001`번 포트에 공개됐으며 MySQL과 Redis는 Compose 내부 네트워크에서만 접근할 수 있다.

### Flask 정상 모드 확인

```console
$ curl http://localhost:5001

    <h1>My First Compose</h1>
    <p>서비스를 이용할 수 있습니다.</p>
    <p>로그인하세요.</p>
    ...
    <p>mode=normal</p>
```

Dockerfile의 `APP_MODE=normal`이 Flask 응답에 반영됐다. 이후 Compose에서 `APP_MODE=maintenance`를 주입해 로그인 시도 차단과 점검 안내가 표시되는 것도 확인한 뒤 정상 모드로 복구했다.

### Compose 종료

```console
$ docker compose down
[+] Running 4/4
 ✔ Container my-first-compose-app-1    Removed
 ✔ Container my-first-compose-mysql-1  Removed
 ✔ Container my-first-compose-redis-1  Removed
 ✔ Network my-first-compose_default    Removed
```

세 컨테이너와 Compose 네트워크를 정리했다. `docker compose down`에 `-v` 옵션을 사용하지 않았으므로 MySQL 데이터가 저장된 Named Volume은 유지된다.
