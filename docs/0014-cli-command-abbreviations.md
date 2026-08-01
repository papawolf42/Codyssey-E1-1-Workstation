# CLI 명령어·옵션 약어 사전

> 범위: `instruction.md`와 개발 워크스테이션 실습에 등장하는 터미널, 권한, Docker, Git 명령어

## 먼저 답: `docker ps`의 `ps`는?

`ps`는 Unix 명령어에서 보통 **process status**라고 풀이한다.

```bash
docker ps
```

Docker에서는 호스트의 일반 프로세스가 아니라 **실행 중인 컨테이너 목록과 상태**를 보여준다.

```bash
docker ps -a
```

`-a`는 **all**의 약어로, 중지된 컨테이너까지 모두 표시한다.

참고로 현재 Docker CLI에는 의미가 더 명확한 다음 명령도 있다.

```bash
docker container ls
```

이 명령은 `docker ps`와 같은 역할을 한다. 여기서 `ls`는 **list**다.

---

## 1. CLI 기본 용어

| 용어 | 원형 | 뜻 |
|---|---|---|
| CLI | Command-Line Interface | 명령줄 인터페이스 |
| GUI | Graphical User Interface | 그래픽 사용자 인터페이스 |
| shell | 고유명사에 가까움 | 명령을 해석해 운영체제에 전달하는 프로그램 |
| bash | Bourne Again Shell | Bourne shell을 개선한 셸 |
| zsh | Z Shell | Z라는 이름의 셸 |
| stdin | standard input | 표준 입력 |
| stdout | standard output | 표준 출력 |
| stderr | standard error | 표준 오류 출력 |
| TTY | teletypewriter | 터미널 장치를 가리키는 역사적 명칭 |
| PID | Process ID | 프로세스 식별 번호 |

---

## 2. 터미널 명령어 이름

일부 Unix 명령은 공식적으로 약어이며, 일부는 이름의 유래를 관습적으로 풀어 설명한다.

| 명령 | 원형·유래 | 역할 |
|---|---|---|
| `pwd` | print working directory | 현재 작업 디렉토리 출력 |
| `ls` | list | 파일·디렉토리 목록 출력 |
| `cd` | change directory | 작업 디렉토리 이동 |
| `mkdir` | make directory | 디렉토리 생성 |
| `rmdir` | remove directory | 빈 디렉토리 삭제 |
| `cp` | copy | 파일·디렉토리 복사 |
| `mv` | move | 파일 이동 또는 이름 변경 |
| `rm` | remove | 파일·디렉토리 삭제 |
| `cat` | concatenate | 파일을 이어 붙여 출력 |
| `touch` | touch | 파일의 시간 정보를 갱신하며, 없으면 빈 파일 생성 |
| `echo` | echo | 문자열이나 변수 값을 출력 |
| `sh` | shell | 기본 명령 셸 실행 |
| `ps` | process status | 프로세스 상태·목록 출력 |
| `curl` | client URL | URL을 이용해 서버와 데이터 송수신 |
| `sed` | stream editor | 입력 스트림의 텍스트 변환·선택 |
| `grep` | global regular expression print | 패턴과 일치하는 줄 검색 |
| `man` | manual | 명령어 설명서 출력 |

### `cat`은 왜 고양이가 아닌가?

`cat`은 **concatenate**, 즉 여러 파일을 이어 붙인다는 말에서 왔다.

```bash
cat a.txt b.txt
```

두 파일의 내용을 순서대로 표준 출력에 보낸다. 파일 하나의 내용을 확인할 때도 자주 사용한다.

### `touch`는 무엇을 만지는가?

원래 목적은 파일의 접근·수정 시간을 갱신하는 것이다.

```bash
touch memo.txt
```

파일이 없으면 빈 파일이 만들어지기 때문에 빈 파일 생성 명령으로도 널리 사용한다.

---

## 3. 터미널 옵션 약어

옵션은 같은 글자라도 명령에 따라 뜻이 달라질 수 있다. 반드시 **명령과 함께** 외워야 한다.

### `ls`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-a` | all | `.`으로 시작하는 숨김 항목까지 표시 |
| `-l` | long format | 권한·소유자·크기 등을 상세 형식으로 표시 |
| `-h` | human-readable | 크기를 KB, MB처럼 읽기 쉽게 표시 |
| `-d` | directory | 디렉토리 내부가 아니라 디렉토리 자체 표시 |
| `-R` | recursive | 하위 디렉토리까지 재귀적으로 표시 |

```bash
ls -la
ls -lh
ls -ld directory
```

여러 짧은 옵션은 `-l -a` 대신 `-la`처럼 합칠 수 있다.

### `mkdir`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-p` | parents | 필요한 상위 디렉토리까지 함께 생성 |

```bash
mkdir -p a/b/c
```

### `cp`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-R`, `-r` | recursive | 디렉토리와 하위 내용을 재귀적으로 복사 |
| `-i` | interactive | 덮어쓰기 전에 확인 |
| `-v` | verbose | 처리 중인 대상을 자세히 출력 |

### `mv`, `rm`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-i` | interactive | 덮어쓰기·삭제 전에 확인 |
| `-f` | force | 확인 없이 강제 처리 |
| `-r`, `-R` | recursive | `rm`에서 디렉토리 하위를 재귀적으로 삭제 |
| `-v` | verbose | 처리 내용을 자세히 출력 |

`rm -rf`는 다음 두 옵션의 조합이다.

```text
-r = recursive
-f = force
```

대상을 잘못 지정하면 큰 피해가 발생할 수 있으므로 시험에서는 의미를 이해하되 실제 사용은 신중해야 한다.

### `curl`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-i` | include | HTTP 응답 헤더를 본문과 함께 출력 |
| `-I` | head | 헤더만 요청·출력 |
| `-s` | silent | 진행률과 일반 오류 메시지 숨김 |
| `-S` | show-error | `-s` 사용 중에도 오류는 표시 |
| `-L` | location | 리다이렉션을 따라감 |
| `-o` | output | 출력을 지정 파일에 저장 |
| `-X` | request | HTTP 메서드를 직접 지정 |

```bash
curl -i http://localhost:8080
curl -sS http://localhost:8080
```

`-sS`는 진행률은 숨기되 오류는 보여 달라는 조합이다.

---

## 4. 권한 명령어

| 명령 | 원형 | 역할 |
|---|---|---|
| `chmod` | change mode | 파일·디렉토리의 권한 모드 변경 |
| `chown` | change owner | 소유자 변경 |
| `chgrp` | change group | 소유 그룹 변경 |

```bash
chmod 644 file.txt
chmod 755 directory
```

권한 문자:

| 문자 | 원형 | 숫자 | 의미 |
|---|---|---:|---|
| `r` | read | 4 | 읽기 |
| `w` | write | 2 | 쓰기 |
| `x` | execute | 1 | 파일 실행 또는 디렉토리 진입 |

사용자 범위:

| 문자 | 원형 | 의미 |
|---|---|---|
| `u` | user | 소유자 |
| `g` | group | 소유 그룹 |
| `o` | others | 기타 사용자 |
| `a` | all | 모든 사용자 |

```bash
chmod u+x script.sh
chmod g-w file.txt
chmod a+r file.txt
```

---

## 5. Docker 자체 용어

| 용어 | 원형 | 뜻 |
|---|---|---|
| Docker CLI | Docker Command-Line Interface | Docker에 명령을 내리는 터미널 도구 |
| API | Application Programming Interface | 프로그램 간 기능을 요청·응답하는 인터페이스 |
| ID | Identifier | 이미지·컨테이너 등의 식별자 |
| OCI | Open Container Initiative | 컨테이너 이미지·런타임 표준 단체 |
| CPU | Central Processing Unit | 중앙 처리 장치 |
| MEM | memory | 메모리 |
| NET I/O | network input/output | 네트워크 입출력 |
| BLOCK I/O | block input/output | 디스크 계열 블록 장치 입출력 |

---

## 6. Docker 명령어 이름

Docker의 하위 명령 대부분은 영어 단어 그대로이며, 축약 명령도 함께 제공한다.

| 명령 | 원형·뜻 | 역할 |
|---|---|---|
| `docker ps` | process status | 컨테이너 목록·상태 확인 |
| `docker container ls` | list | 컨테이너 목록 확인 |
| `docker images` | images | 이미지 목록 확인 |
| `docker image ls` | list | 이미지 목록 확인 |
| `docker pull` | pull | 레지스트리에서 이미지 받기 |
| `docker build` | build | Dockerfile로 이미지 생성 |
| `docker run` | run | 이미지에서 새 컨테이너 생성·실행 |
| `docker start` | start | 기존 컨테이너 시작 |
| `docker stop` | stop | 실행 중인 컨테이너 정상 중지 |
| `docker restart` | restart | 컨테이너 재시작 |
| `docker exec` | execute | 실행 중인 컨테이너에서 새 명령 실행 |
| `docker attach` | attach | 컨테이너의 기존 주 프로세스에 연결 |
| `docker logs` | logs | 컨테이너 로그 출력 |
| `docker stats` | statistics | 리소스 사용 통계 출력 |
| `docker inspect` | inspect | 객체의 상세 설정·상태 출력 |
| `docker port` | port | 컨테이너의 포트 매핑 출력 |
| `docker rm` | remove | 컨테이너 삭제 |
| `docker rmi` | remove image | 이미지 삭제 |
| `docker cp` | copy | 호스트와 컨테이너 사이 파일 복사 |
| `docker info` | information | Docker 클라이언트·서버 정보 출력 |
| `docker version` | version | 클라이언트·서버 버전 정보 출력 |

### 축약 명령 대응표

| 짧은 명령 | 구조가 명확한 명령 |
|---|---|
| `docker ps` | `docker container ls` |
| `docker images` | `docker image ls` |
| `docker rm` | `docker container rm` |
| `docker rmi` | `docker image rm` |

---

## 7. `docker run` 옵션 약어

```bash
docker run -dit \
  --name ubuntu-container \
  -p 8080:80 \
  -v mydata:/data \
  ubuntu bash
```

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-d` | detach / detached | 백그라운드 실행 |
| `-i` | interactive | 표준 입력을 열린 상태로 유지 |
| `-t` | TTY | 가상 터미널 할당 |
| `--name` | name | 컨테이너 이름 지정 |
| `-p` | publish | 호스트에 컨테이너 포트 게시 |
| `-P` | publish-all | 노출된 포트를 임의의 호스트 포트에 모두 게시 |
| `-v` | volume | 바인드 마운트 또는 볼륨 연결 |
| `-e` | environment | 환경 변수 설정 |
| `-w` | workdir | 컨테이너 내부 작업 디렉토리 설정 |
| `--rm` | remove | 컨테이너 종료 시 자동 삭제 |
| `--entrypoint` | entry point | 이미지의 기본 진입 명령 변경 |

### 자주 묻는 조합

```text
-it  = interactive + TTY
-dit = detached + interactive + TTY
```

`-it`는 대화형 셸에 주로 사용한다.

```bash
docker run -it ubuntu bash
```

`-d`는 웹 서버처럼 백그라운드에서 계속 동작할 서비스에 사용한다.

```bash
docker run -d nginx:alpine
```

### 포트 표기

```text
-p 8080:80
   └┬─┘ └┬┘
  host container
```

`-p`는 **publish**이며, 왼쪽은 호스트 포트, 오른쪽은 컨테이너 포트다.

### 볼륨 표기

```text
-v mydata:/data
   └─┬──┘ └─┬─┘
    volume container path
```

`-v`는 **volume**이다. 왼쪽에는 볼륨 이름 또는 호스트 경로, 오른쪽에는 컨테이너 경로를 쓴다.

---

## 8. 다른 Docker 옵션

### `docker ps`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-a` | all | 중지된 컨테이너까지 모두 표시 |
| `-q` | quiet | 컨테이너 ID만 출력 |
| `-s` | size | 컨테이너 파일 크기 표시 |
| `-f` | filter | 조건에 맞는 컨테이너만 표시 |
| `--format` | format | 출력 형식 지정 |

```bash
docker ps -a
docker ps -aq
docker ps --format '{{.Names}}'
```

`-aq`는 `all + quiet`이므로 모든 컨테이너의 ID만 출력한다.

### `docker build`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-t` | tag | 이미지 이름과 태그 지정 |
| `-f` | file | 사용할 Dockerfile 경로 지정 |
| `--no-cache` | no cache | 기존 빌드 캐시를 사용하지 않음 |
| `--pull` | pull | 최신 베이스 이미지 확인 |

```bash
docker build -t first-built-image .
```

주의: `docker build`의 `-t`는 여기서 TTY가 아니라 **tag**다. 같은 글자라도 명령에 따라 의미가 다르다.

### `docker exec`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-i` | interactive | 표준 입력 유지 |
| `-t` | TTY | 가상 터미널 할당 |
| `-d` | detach | 명령을 백그라운드에서 실행 |
| `-e` | environment | 환경 변수 설정 |
| `-w` | workdir | 작업 디렉토리 지정 |

```bash
docker exec -it first-nginx-container sh
```

### `docker logs`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-f` | follow | 새 로그를 계속 추적 |
| `-t` | timestamps | 각 로그에 시간 표시 |
| `-n` | number | 마지막 N개 로그 출력 |
| `--tail` | tail | 마지막부터 지정한 개수만 출력 |
| `--since` | since | 지정 시점 이후 로그 출력 |

```bash
docker logs -f first-nginx-container
docker logs --tail 20 first-nginx-container
```

### `docker stats`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `--no-stream` | no stream | 실시간 갱신 없이 한 번만 출력 |
| `-a` | all | 실행 중이 아닌 컨테이너도 표시 |

```bash
docker stats --no-stream first-nginx-container
```

### `docker rm`

| 옵션 | 원형 | 역할 |
|---|---|---|
| `-f` | force | 실행 중인 컨테이너도 강제 삭제 |
| `-v` | volumes | 컨테이너와 연결된 익명 볼륨도 삭제 |

```bash
docker rm -f vol-test
```

이 명령은 컨테이너를 강제 삭제한다. 이름 있는 볼륨은 별도의 `docker volume rm` 명령으로 관리한다.

---

## 9. Dockerfile 명령어 이름

Dockerfile 명령은 축약어보다 영어 키워드 자체인 경우가 많다.

| 명령 | 원형·뜻 | 역할 |
|---|---|---|
| `FROM` | from | 베이스 이미지 지정 |
| `RUN` | run | 이미지 빌드 중 명령 실행 |
| `COPY` | copy | 빌드 컨텍스트의 파일 복사 |
| `ADD` | add | 파일·URL·압축 파일 추가 기능 |
| `CMD` | command | 컨테이너의 기본 명령·인자 지정 |
| `ENTRYPOINT` | entry point | 컨테이너의 주 실행 프로그램 지정 |
| `ENV` | environment | 환경 변수 지정 |
| `ARG` | argument | 빌드 시 사용할 변수 지정 |
| `WORKDIR` | working directory | 이후 명령의 작업 디렉토리 지정 |
| `EXPOSE` | expose | 사용 예정 컨테이너 포트 문서화 |
| `VOLUME` | volume | 외부 저장소 연결 대상 경로 선언 |
| `USER` | user | 이후 명령·실행에 사용할 사용자 지정 |
| `LABEL` | label | 이미지 메타데이터 추가 |
| `HEALTHCHECK` | health check | 컨테이너 상태 확인 방법 지정 |

중요:

```text
CMD = command
ENV = environment
ARG = argument
WORKDIR = working directory
```

`EXPOSE`는 실제 포트 연결이 아니다. 실행할 때 `docker run -p`가 필요하다.

---

## 10. Docker Compose

| 명령 | 뜻 | 역할 |
|---|---|---|
| `docker compose up` | up | 서비스 생성·실행 |
| `docker compose down` | down | 서비스 컨테이너·네트워크 정리 |
| `docker compose ps` | process status | 서비스 컨테이너 상태 확인 |
| `docker compose logs` | logs | 서비스 로그 출력 |
| `docker compose exec` | execute | 서비스 컨테이너에서 명령 실행 |

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

`-d`는 Docker Compose에서도 **detached**, 즉 백그라운드 실행이다.

---

## 11. Git 명령어 이름

Git의 하위 명령은 대부분 축약어가 아니라 영어 단어 그대로다.

| 명령 | 뜻 | 역할 |
|---|---|---|
| `git init` | initialize | 현재 디렉토리에 Git 저장소 생성 |
| `git status` | status | 작업 트리와 스테이징 상태 확인 |
| `git add` | add | 변경 내용을 스테이징 영역에 추가 |
| `git commit` | commit | 스테이징 내용을 로컬 이력으로 기록 |
| `git log` | log | 커밋 이력 확인 |
| `git diff` | difference | 변경 내용의 차이 확인 |
| `git branch` | branch | 브랜치 확인·생성·관리 |
| `git switch` | switch | 브랜치 전환 |
| `git checkout` | check out | 브랜치 전환 또는 파일 상태 복원 |
| `git merge` | merge | 다른 브랜치의 이력 병합 |
| `git remote` | remote | 원격 저장소 정보 관리 |
| `git clone` | clone | 원격 저장소 복제 |
| `git fetch` | fetch | 원격 이력을 내려받되 병합하지 않음 |
| `git pull` | pull | 원격 이력을 내려받아 현재 브랜치에 통합 |
| `git push` | push | 로컬 커밋을 원격으로 전송 |
| `git config` | configuration | Git 설정 확인·변경 |

관련 약어:

| 용어 | 원형 | 의미 |
|---|---|---|
| SCM | Source Code Management | 소스 코드 관리 |
| VCS | Version Control System | 버전 관리 시스템 |
| SHA | Secure Hash Algorithm | Git 객체 식별에 사용되는 해시 계열 |
| URL | Uniform Resource Locator | 원격 저장소 주소 |
| SSH | Secure Shell | 암호화된 원격 접속·인증 방식 |
| HTTPS | Hypertext Transfer Protocol Secure | TLS로 보호되는 HTTP |

---

## 12. Git 옵션 약어

| 옵션 | 주로 사용하는 명령 | 원형 | 역할 |
|---|---|---|---|
| `-m` | `commit` | message | 커밋 메시지 직접 지정 |
| `-a` | `commit` | all | 추적 중인 변경 파일을 자동 스테이징 |
| `-b` | `switch`, `checkout` | branch | 새 브랜치를 만들며 전환 |
| `-d` | `branch` | delete | 병합된 브랜치 삭제 |
| `-D` | `branch` | 강제 delete | 병합 여부와 관계없이 브랜치 강제 삭제 |
| `-M` | `branch` | 강제 move | 브랜치 이름 강제 변경 |
| `-u` | `push` | set upstream | 현재 브랜치의 원격 추적 대상 설정 |
| `-v` | `remote` | verbose | 원격 주소를 자세히 출력 |
| `--global` | `config` | global | 사용자 전체 Git 설정에 적용 |
| `--local` | `config` | local | 현재 저장소 설정에 적용 |
| `--oneline` | `log` | one line | 커밋 하나를 한 줄로 표시 |
| `--graph` | `log` | graph | 브랜치 흐름을 문자 그래프로 표시 |

```bash
git commit -m "Add cheat sheet"
git branch -M main
git push -u origin main
git remote -v
git log --oneline --graph
```

`git branch -M main`에서 `-M`은 현재 브랜치 이름을 `main`으로 강제 변경한다.

---

## 13. 같은 옵션 글자, 다른 의미

옵션의 뜻은 전역적으로 고정되지 않는다.

| 예시 | 의미 |
|---|---|
| `ls -a` | all |
| `docker ps -a` | all |
| `git commit -a` | all tracked changes |
| `docker run -t` | TTY |
| `docker build -t` | tag |
| `docker logs -t` | timestamps |
| `docker run -p` | publish |
| `mkdir -p` | parents |
| `docker logs -f` | follow |
| `docker rm -f` | force |
| `docker build -f` | file |
| `docker ps -f` | filter |
| `docker rm -v` | volumes |
| `git remote -v` | verbose |

시험에서는 옵션 글자만 외우지 말고 다음처럼 명령 전체로 기억한다.

```text
docker run -t   → TTY
docker build -t → tag
docker logs -t  → timestamps
```

---

## 14. 시험 직전 초압축 암기표

```text
pwd     print working directory
ls      list
cd      change directory
mkdir   make directory
cp      copy
mv      move
rm      remove
cat     concatenate
chmod   change mode

ps      process status
docker ps -a        all containers
docker run -d       detached
docker run -i       interactive
docker run -t       TTY
docker run -p       publish port
docker run -v       volume
docker build -t     tag
docker exec         execute
docker stats        statistics
docker rmi          remove image

CMD     command
ENV     environment
ARG     argument
WORKDIR working directory

git init             initialize
git diff             difference
git config           configuration
git commit -m        message
git branch -M        rename branch forcibly
git push -u          set upstream
git remote -v        verbose
```

## 최종 기억법

> 명령어 이름은 “무엇을 할지”를 말하고, 옵션은 “어떻게 할지”를 바꾼다. 단, 같은 옵션 글자라도 명령마다 뜻이 다르므로 `docker run -t`, `docker build -t`, `docker logs -t`처럼 명령과 옵션을 한 묶음으로 외운다.
