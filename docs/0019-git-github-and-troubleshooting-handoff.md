# Git·GitHub 및 트러블슈팅 후속 작업 인계

## 1. 현재 완료 상태

- Docker 설치 및 기본 운영 완료
- Dockerfile 기반 `first-built-image` 빌드 완료
- `first-container` 포트 매핑 실습 완료
- 파일·디렉터리 권한 변경 실습 완료
- 바인드 마운트 반영 실습 완료
- Docker 볼륨 영속성 실습 완료
- 바인드 마운트 기록은 커밋 `22b8131`로 `main`에 반영됨
- 볼륨 영속성 기록은 커밋 `629cfaa`로 `main`에 반영됨

현재 수행 체크리스트에서 남은 큰 항목은 `Git 설정 + VSCode GitHub 연동`이다. 이 항목을 마친 뒤 기술 문서의 별도 필수 조건인 트러블슈팅 2건을 정리하고 최종 점검한다.

## 2. 집에서 다시 시작할 때

원격 브랜치 정보를 받은 뒤 운반용 브랜치가 아니라 실제 제출 브랜치에서 작업한다.

```bash
git fetch origin
git switch main
git pull --ff-only origin main
```

## 3. 지시문에 따른 Git 작업

`instruction.md`에서 직접 요구한 범위는 Git 사용자 정보와 기본 브랜치 설정, `git config --list` 결과 기록이다.

```bash
git branch -M main
git config --list
```

현재 저장소에 설정한 사용자 정보는 다음과 같다.

```text
user.name=gunkim
user.email=68710498+papawolf42@users.noreply.github.com
```

`git config --list` 결과를 README에 기록하기 전에 토큰, 비밀번호, 개인키, 인증 코드 등 민감정보가 없는지 확인하고 필요한 경우 마스킹한다.

## 4. VS Code와 GitHub 연동

1. VS Code에서 이 저장소를 연다.
2. GitHub 계정 로그인을 확인한다.
3. 현재 저장소가 GitHub 원격 저장소와 연동됐는지 확인한다.
4. Source Control과 연동 상태가 보이는 화면을 캡처한다.
5. 캡처에 토큰, 비밀번호, 인증 코드가 없는지 확인한다.
6. 이미지를 다음 경로에 저장한다.

```text
mandatory/screenshots/05-vscode-github.png
```

README에는 Git은 로컬 버전 관리 도구이고 GitHub는 Git 저장소를 원격에 보관하며 공유·협업하는 플랫폼이라는 차이도 설명한다.

## 5. 트러블슈팅 요구사항

`instruction.md`의 직접 요구는 다음과 같다.

```text
트러블슈팅 2건 이상
문제 → 원인 가설 → 확인 → 해결/대안
```

각 사례에는 실제 명령과 출력 결과를 함께 기록한다. 전용 스크린샷은 필수가 아니며 README만 보고 확인 절차를 재현할 수 있어야 한다.

### 사례 1: Nginx 권한 문제

파일 권한 `600`과 디렉터리 권한 `644`로 인해 발생한 HTTP 403을 하나의 사례로 묶는다.

- 문제: Nginx가 `403 Forbidden` 반환
- 원인 가설: Nginx 작업 프로세스에 파일 읽기 권한 또는 디렉터리 진입 권한이 없음
- 확인: `ls -l`, `ls -ld`, `curl`, `docker logs` 사용
- 해결: 파일을 `644`, 디렉터리를 `755`로 복구
- 검증: `curl`에서 `HTTP/1.1 200 OK` 확인

실제 출력은 `mandatory/README.md`의 권한 변경 실습과 `docs/0010-permission-practice-raw-log.md`에 이미 기록돼 있다.

### 사례 2: foreground 컨테이너 실행

아직 실제 수행 로그를 만들지 않았다. 다음 작업일에 직접 수행한 뒤 관찰 결과만 기록한다.

기존 포트 8080, 8081, 8082와 겹치지 않게 8083을 사용한다.

```bash
docker run --name foreground_container -p 8083:80 first-built-image
```

관찰할 내용:

- `-d` 없이 실행하면 Nginx가 foreground로 실행되어 터미널을 점유한다.
- 이는 컨테이너가 다운된 상태가 아니다.
- 다른 터미널에서 `docker ps`와 `curl http://localhost:8083`으로 실행 상태를 확인한다.
- 첫 번째 터미널에서 `Ctrl+C`를 입력하면 Nginx 메인 프로세스가 종료되어 컨테이너도 종료되는지 확인한다.

확인 명령:

```bash
docker ps -a --filter name=foreground_container
```

종료된 컨테이너를 삭제하고 `-d` 옵션으로 다시 실행한다.

```bash
docker rm foreground_container
docker run -d --name foreground_container -p 8083:80 first-built-image
docker ps --filter name=foreground_container
curl http://localhost:8083
```

README에는 `-d`가 컨테이너를 강제로 유지하는 옵션이 아니라 터미널에서 분리해 백그라운드로 실행하는 옵션이라고 정확히 설명한다. 컨테이너의 유지 여부는 메인 프로세스가 실행 중인지에 따라 결정된다.

## 6. 마지막 점검 순서

1. 원격 `main`의 최신 진행사항 받기
2. Git 기본 브랜치 설정 및 `git config --list` 결과 기록
3. VS Code·GitHub 연동 확인과 `05-vscode-github.png` 추가
4. Git과 GitHub의 역할 차이 작성
5. foreground 실행 트러블슈팅 실제 수행
6. 트러블슈팅 2건을 README에 작성
7. 수행 체크리스트 완료 여부 확인
8. 로그와 이미지의 민감정보 확인
9. 최종 커밋 및 푸시

## 7. 현재 Docker 실습 상태

현재 환경에서는 다음 상태로 구성했다. 다른 컴퓨터에서는 Docker 이미지와 컨테이너가 Git으로 이동하지 않으므로 필요하면 Dockerfile과 README 명령으로 재구성한다.

- `first-built-image`: 커스텀 Nginx 이미지
- `first-container`: 호스트 8080번 포트
- `bind_container`: 호스트 8081번 포트, 호스트 `site` 디렉터리 바인드 마운트
- `volume_container2`: 호스트 8082번 포트, `docker-volume` 연결
- `docker-volume`: 변경된 `index.html` 영속 저장

Docker 상태 확인:

```bash
docker images
docker ps -a
docker volume ls
```
