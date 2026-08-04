# Codyssey E1-1 Workstation — 보너스 체크리스트

## 목표

- [ ] Flask, MySQL, Redis 세 컨테이너 사용
- [ ] MySQL에 사용자 ID와 비밀번호 해시 저장
- [ ] Redis에 접속 시각과 TTL 10초 세션 저장
- [ ] 10초 동안 이용하지 않으면 재로그인 안내

## 1) 파일 준비

- [x] `compose.yaml`
- [ ] `app.py`
- [ ] `Dockerfile`
- [ ] `requirements.txt`

## 2) 보너스 1 — 단일 서비스

- [x] MySQL만 실행 — `docker compose up -d mysql`
- [x] 상태 확인 — `docker compose ps`
- [ ] 단일 서비스 종료 — `docker compose down`

## 3) 보너스 2 — 멀티 컨테이너

- [ ] Flask, MySQL, Redis 실행 — `docker compose up -d --build`
- [ ] 세 컨테이너 상태 확인 — `docker compose ps`
- [ ] Flask가 서비스 이름 `mysql`로 MySQL에 연결
- [ ] Flask가 서비스 이름 `redis`로 Redis에 연결
- [ ] Flask 포트만 호스트에 공개
- [ ] MySQL과 Redis 포트는 호스트에 공개하지 않음

## 4) 로그인 세션

- [ ] MySQL에 테스트 사용자 ID 저장
- [ ] 비밀번호 원문 대신 해시 저장
- [ ] 로그인 시 ID와 비밀번호 확인
- [ ] 로그인 성공 시 Redis 세션 생성
- [ ] Redis에 사용자 ID와 접속 시각 저장
- [ ] 세션 TTL을 10초로 설정
- [ ] 로그인 상태에서 요청하면 TTL을 다시 10초로 갱신
- [ ] 10초 동안 요청하지 않으면 세션 자동 삭제
- [ ] `세션이 만료되었습니다. 다시 로그인하세요.` 표시
- [ ] 재로그인 성공 확인

## 5) 보너스 3 — 운영 명령

- [ ] 실행 — `docker compose up -d`
- [ ] 상태 — `docker compose ps`
- [ ] 로그 — `docker compose logs`
- [ ] 종료 — `docker compose down`
- [ ] Compose 운영 명령과 실행 결과를 README에 기록

## 6) 보너스 4 — 환경변수

- [ ] `APP_MODE=study`를 앱에 주입
- [ ] 응답에서 `mode=study` 확인
- [ ] `APP_MODE=exam`으로 변경
- [ ] 코드 수정 없이 응답이 `mode=exam`으로 변경되는지 확인

## 7) 최종 확인

- [ ] 실제 명령과 출력이 README에 있음
- [ ] 비밀번호 원문과 세션 Token을 출력하지 않음
- [ ] `docker compose down`으로 실습 컨테이너 정리

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
