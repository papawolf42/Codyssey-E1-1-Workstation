# Codyssey E1-1 Workstation — 필수 체크리스트

## 2) 수행 체크리스트

- [ ] 터미널 기본 조작 및 폴더 구성
    - [ ] 현재 위치 확인 — `pwd`
    - [ ] 목록 확인(숨김 파일 포함) — `ls -la`
    - [ ] 디렉토리 이동 — `cd <directory>`
    - [ ] 디렉토리·파일 생성 — `mkdir`, `touch`
    - [ ] 파일 내용 확인 — `cat <file>`
    - [ ] 파일 복사 — `cp <source> <destination>`
    - [ ] 파일 이동·이름 변경 — `mv <source> <destination>`
    - [ ] 파일·디렉토리 삭제 — `rm`, `rmdir`
    - [ ] 빈 파일 생성 — `touch <empty_file>`
    - [ ] 명령어와 출력 결과 기록

- [ ] 권한 변경 실습
    - [ ] 파일 1개의 권한 확인 및 변경 — `ls -l`, `chmod`
    - [ ] 디렉토리 1개의 권한 확인 및 변경 — `ls -ld`, `chmod`
    - [ ] 변경 전·후 비교 기록
    - [ ] `r/w/x`, `755`, `644`의 의미 설명

- [ ] Docker 설치/점검
    - [ ] Docker 실행 환경 확인 — 서울 환경: OrbStack
    - [ ] Docker 버전 확인 — `docker --version`
    - [ ] Docker 데몬 동작 여부 확인 — `docker info`
    - [ ] Docker CLI와 데몬이 정상적으로 연결되는지 확인

- [ ] Docker 기본 운영
    - [ ] 이미지 다운로드 및 목록 확인 — `docker pull`, `docker images`
    - [ ] 컨테이너 실행·중지·목록 확인 — `docker run`, `docker stop`, `docker ps`, `docker ps -a`
    - [ ] 컨테이너 로그 확인 — `docker logs <container>`
    - [ ] 컨테이너 리소스 확인 — `docker stats --no-stream <container>`
    - [ ] 기본 운영 명령과 핵심 출력 결과 기록

- [ ] hello-world 실행
    - [ ] 공식 테스트 이미지 실행 — `docker run hello-world`
    - [ ] 실행 성공 결과 기록
    - [ ] `ubuntu` 컨테이너 실행 및 내부 진입 — `docker run -it ubuntu bash`
    - [ ] 컨테이너 내부에서 간단한 명령 실행 — `ls`, `echo`
    - [ ] `attach`와 `exec`의 차이 관찰 — `docker attach`, `docker exec`
    - [ ] 컨테이너 종료·유지 방식의 차이 정리

- [ ] Dockerfile 빌드/실행
    - [ ] 커스텀 이미지 제작 방식 선택: 웹 서버 베이스 또는 Linux 베이스
    - [ ] 베이스 이미지와 선택 이유 기록
    - [ ] 웹 서버 소스코드 작성 — 예: `site/`, `app/`, `src/`
    - [ ] Dockerfile 작성 — `Dockerfile`
    - [ ] 적용한 커스텀 포인트와 목적 설명
    - [ ] 이미지 빌드 — `docker build -t <image>:<tag> .`
    - [ ] 커스텀 이미지 실행 — `docker run`
    - [ ] 빌드·실행 명령과 핵심 결과 기록

- [ ] 포트 매핑 접속
    - [ ] 호스트 포트와 컨테이너 포트 연결 — `-p <host_port>:<container_port>`
    - [ ] 컨테이너 내부 서비스 포트 확인
    - [ ] 브라우저 접속 또는 `curl` 응답 확인 — `curl http://localhost:<host_port>`
    - [ ] 브라우저 사용 시 주소창과 응답 화면 기록
    - [ ] 포트 매핑이 필요한 이유 설명
    - [ ] 포트 매핑 접속 스크린샷 또는 `curl` 결과 기록

- [ ] 바인드 마운트 반영
    - [ ] 호스트 파일의 변경 전 내용 확인
    - [ ] 바인드 마운트로 컨테이너 실행 — `docker run -v <host_path>:<container_path>`
    - [ ] 호스트 파일 변경
    - [ ] 컨테이너 또는 브라우저에서 변경 반영 확인
    - [ ] 실행 명령과 호스트 변경 전·후 결과 기록

- [ ] 볼륨 영속성
    - [ ] Docker 볼륨 생성 — `docker volume create <volume>`
    - [ ] 볼륨을 컨테이너에 연결 — `docker run -v <volume>:<container_path>`
    - [ ] 볼륨에 데이터 기록 및 확인 — `docker exec`
    - [ ] 컨테이너 삭제 — `docker rm`
    - [ ] 같은 볼륨으로 새 컨테이너 실행
    - [ ] 새 컨테이너에서 기존 데이터 확인
    - [ ] 컨테이너 삭제 전·후 비교 기록
    - [ ] Docker 볼륨과 영속 데이터 설명

- [ ] Git 설정 + VSCode GitHub 연동
    - [ ] Git 사용자 정보 설정 — `git config user.name`, `git config user.email`
    - [ ] 기본 브랜치 설정 — `git branch -M main`
    - [ ] Git 설정 결과 기록 — `git config --list`
    - [ ] VSCode에서 GitHub 로그인
    - [ ] VSCode와 GitHub 저장소 연동
    - [ ] GitHub 저장소 링크와 접근 가능 여부 확인
    - [ ] Git과 GitHub의 역할 차이 설명
    - [ ] ID·비밀번호·토큰 등 민감정보 미포함 확인
