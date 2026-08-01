# 개발 워크스테이션 시험 전날 총정리

> 범위: `instruction.md` 전체  
> 목표: 명령어를 외우는 데서 끝나지 않고, **왜 필요한지 설명하고 상황에 맞는 명령을 고르는 것**

## 0. 시험 직전 핵심 12문장

1. 절대 경로는 루트(`/`)부터 시작하는 전체 주소이고, 상대 경로는 현재 작업 디렉토리를 기준으로 한 주소다.
2. `pwd`는 현재 위치, `ls -la`는 숨김 파일을 포함한 상세 목록, `cd`는 디렉토리 이동 명령이다.
3. 권한은 소유자·그룹·기타 사용자 순서이며, `r=4`, `w=2`, `x=1`을 더해 숫자로 나타낸다.
4. 일반 파일의 `x`는 실행, 디렉토리의 `x`는 진입과 내부 항목 접근 권한이다.
5. Docker 이미지는 실행 환경을 담은 불변 템플릿이고, 컨테이너는 이미지로 만든 실행 인스턴스다.
6. Dockerfile은 이미지를 만드는 설계도이며, `docker build`는 이미지 생성, `docker run`은 컨테이너 생성과 실행이다.
7. `EXPOSE 80`은 이미지가 사용할 포트를 설명할 뿐, 호스트에 포트를 실제로 공개하지 않는다.
8. `-p 8080:80`은 호스트의 8080번 포트를 컨테이너의 80번 포트에 연결한다.
9. 바인드 마운트는 호스트 경로를 직접 연결하고, Docker 볼륨은 Docker가 관리하는 저장 공간을 연결한다.
10. 컨테이너를 삭제해도 별도 볼륨의 데이터는 유지되므로 새 컨테이너에 다시 연결할 수 있다.
11. Git은 로컬 버전 관리 도구이고, GitHub는 Git 저장소를 원격에서 공유·협업하는 플랫폼이다.
12. 설치 확인과 동작 확인은 다르다. `docker --version`은 CLI 설치를, `docker info`의 Server 정보는 엔진 연결을 확인한다.

---

## 1. 터미널과 경로

### 1-1. 절대 경로와 상대 경로

현재 위치가 `/Users/me/project`라고 가정한다.

| 구분 | 예시 | 의미 |
|---|---|---|
| 절대 경로 | `/Users/me/project/site/index.html` | 루트부터 시작하는 고정된 전체 경로 |
| 상대 경로 | `site/index.html` | 현재 위치를 기준으로 찾는 경로 |
| 현재 디렉토리 | `./site/index.html` | `.`은 현재 디렉토리 |
| 상위 디렉토리 | `../README.md` | `..`은 한 단계 위 디렉토리 |
| 홈 디렉토리 | `~/project` | `~`는 현재 사용자의 홈 |

모범 답안:

> 절대 경로는 `/`부터 시작하므로 현재 위치가 달라도 같은 대상을 가리킨다. 상대 경로는 현재 작업 디렉토리를 기준으로 해석되므로 현재 위치가 바뀌면 가리키는 대상도 달라질 수 있다.

### 1-2. 필수 명령어

| 목적 | 명령 | 기억할 점 |
|---|---|---|
| 현재 위치 확인 | `pwd` | print working directory |
| 목록 확인 | `ls` | 현재 디렉토리의 항목 |
| 숨김 파일 포함 상세 목록 | `ls -la` | `-l`: 상세, `-a`: 전체 |
| 디렉토리 이동 | `cd directory` | 상위는 `cd ..` |
| 디렉토리 생성 | `mkdir practice` | 중간 경로까지는 `mkdir -p a/b` |
| 빈 파일 생성/시간 갱신 | `touch file.txt` | 기존 파일 내용은 지우지 않음 |
| 내용 출력 | `cat file.txt` | 짧은 파일 확인에 적합 |
| 복사 | `cp source destination` | 디렉토리는 보통 `cp -R` |
| 이동 또는 이름 변경 | `mv old new` | 같은 위치에서 이름만 바꾸면 rename |
| 파일 삭제 | `rm file.txt` | 휴지통을 거치지 않을 수 있음 |
| 빈 디렉토리 삭제 | `rmdir directory` | 비어 있어야 함 |

### 1-3. 자주 틀리는 부분

- `touch`는 디렉토리가 아니라 파일을 만든다. 디렉토리는 `mkdir`로 만든다.
- `mv`는 이동과 이름 변경을 모두 수행한다.
- `ls`만으로는 `.git` 같은 숨김 항목이 보이지 않는다. `ls -la`를 사용한다.
- 상대 경로 오류가 나면 먼저 `pwd`와 `ls -la`로 현재 위치와 실제 이름을 확인한다.
- `rm`은 파괴적인 명령이므로 삭제 대상을 먼저 `ls`로 확인한다.

---

## 2. 리눅스 파일 권한

### 2-1. 권한 문자열 읽기

```text
-rw-r--r--
││  │  └─ 기타 사용자(other): r--
││  └──── 그룹(group): r--
│└─────── 소유자(user): rw-
└──────── 파일 종류: - 일반 파일, d 디렉토리
```

권한의 의미:

| 권한 | 숫자 | 일반 파일 | 디렉토리 |
|---|---:|---|---|
| `r` | 4 | 내용 읽기 | 내부 항목 이름 목록 보기 |
| `w` | 2 | 내용 수정 | 내부 항목 생성·삭제·이름 변경 |
| `x` | 1 | 실행 | 진입 및 내부 경로 접근 |

디렉토리에서는 `x`가 특히 중요하다. 디렉토리에 읽기 권한이 있어도 실행 권한이 없으면 내부 파일 경로에 정상적으로 접근하지 못할 수 있다.

### 2-2. 숫자 권한 계산

각 사용자 범위에서 `r=4`, `w=2`, `x=1`을 더한다.

| 숫자 | 기호 | 계산 | 의미 |
|---:|---|---|---|
| 7 | `rwx` | 4+2+1 | 읽기·쓰기·실행 |
| 6 | `rw-` | 4+2 | 읽기·쓰기 |
| 5 | `r-x` | 4+1 | 읽기·실행 |
| 4 | `r--` | 4 | 읽기 |
| 0 | `---` | 0 | 권한 없음 |

대표 예:

- `chmod 755 directory`: 소유자는 `rwx`, 그룹과 기타 사용자는 `r-x`
- `chmod 644 file`: 소유자는 `rw-`, 그룹과 기타 사용자는 `r--`
- `chmod 600 secret`: 소유자만 읽고 쓸 수 있음

### 2-3. 확인과 변경

```bash
ls -l file.txt
ls -ld directory
chmod 600 file.txt
chmod 755 directory
```

`ls -ld directory`에서 `-d`가 없으면 디렉토리 자체가 아니라 내부 목록이 출력될 수 있다.

모범 답안:

> `755`는 소유자에게 읽기·쓰기·실행 권한을 주고, 그룹과 기타 사용자에게 읽기·실행 권한을 준다. `644`는 소유자에게 읽기·쓰기를, 나머지 사용자에게 읽기만 허용한다. 디렉토리에는 진입을 위해 `x`가 필요하므로 일반적인 공개 디렉토리에는 `755`, 일반 문서 파일에는 `644`가 자주 사용된다.

---

## 3. Docker의 구조

### 3-1. Docker가 필요한 이유

Docker는 애플리케이션과 실행에 필요한 환경을 이미지로 묶고, 이를 격리된 컨테이너로 실행한다. 개발자마다 OS나 설치 상태가 달라서 생기는 “내 컴퓨터에서는 되는데?” 문제를 줄이고, 같은 이미지를 이용해 재현 가능한 실행 환경을 제공한다.

```text
Dockerfile --docker build--> 이미지 --docker run--> 컨테이너
    설계도                    템플릿              실행 인스턴스
```

### 3-2. 이미지와 컨테이너 비교

| 이미지 | 컨테이너 |
|---|---|
| 실행 환경을 담은 읽기 중심 템플릿 | 이미지로 생성한 실행 인스턴스 |
| 하나의 이미지로 여러 컨테이너 생성 가능 | 실행·중지·삭제 가능 |
| `docker images`로 확인 | `docker ps`, `docker ps -a`로 확인 |
| `docker pull`, `docker build`로 확보 | `docker run`으로 생성·실행 |

모범 답안:

> 이미지는 프로그램과 실행 환경을 담은 템플릿이고, 컨테이너는 그 이미지에서 생성되어 실제로 동작하는 프로세스다. 클래스와 객체, 또는 붕어빵 틀과 붕어빵에 비유할 수 있다.

### 3-3. 설치 확인과 엔진 확인

```bash
docker --version
docker info
```

- `docker --version`: Docker CLI 명령이 설치되어 있는지 확인한다.
- `docker info`: CLI가 Docker 엔진에 연결되는지 확인한다.
- `docker info`에 `Server` 정보가 정상 출력되어야 컨테이너 실행 준비가 된 것이다.
- 서울 캠퍼스처럼 `sudo`가 제한된 환경에서는 OrbStack을 실행해 Docker 엔진을 제공할 수 있다.

### 3-4. 기본 운영 명령

| 목적 | 명령 |
|---|---|
| 이미지 받기 | `docker pull ubuntu` |
| 이미지 목록 | `docker images` |
| 새 컨테이너 생성·실행 | `docker run IMAGE` |
| 실행 중 컨테이너 | `docker ps` |
| 중지된 것까지 전체 컨테이너 | `docker ps -a` |
| 컨테이너 중지 | `docker stop NAME` |
| 기존 컨테이너 시작 | `docker start NAME` |
| 컨테이너 삭제 | `docker rm NAME` |
| 이미지 삭제 | `docker rmi IMAGE` |
| 로그 확인 | `docker logs NAME` |
| 실시간 로그 추적 | `docker logs -f NAME` |
| 리소스 1회 확인 | `docker stats --no-stream NAME` |
| 실행 중 컨테이너에서 새 명령 | `docker exec -it NAME sh` |
| 주 프로세스 입출력에 연결 | `docker attach NAME` |

### 3-5. `docker run`의 정체

`docker run`은 기존 컨테이너를 다시 실행하는 명령이 아니다. 이미지에서 **새 컨테이너를 생성하고 시작**한다. 기존에 만든 컨테이너를 다시 켤 때는 `docker start`를 사용한다.

```bash
docker run -dit --name ubuntu-container ubuntu bash
```

- `-d`: 백그라운드(detached) 실행
- `-i`: 표준 입력을 열어 둠(interactive)
- `-t`: 가상 터미널 할당(TTY)
- `--name`: 컨테이너 이름 지정
- `ubuntu`: 사용할 이미지
- `bash`: 컨테이너의 주 프로세스

### 3-6. 컨테이너 생명주기와 PID 1

컨테이너는 내부의 주 프로세스(PID 1)가 살아 있는 동안 실행된다. `ubuntu` 이미지로 대화형 `bash`를 실행하고 그 셸에서 `exit`하면 주 프로세스가 끝나므로 컨테이너도 중지된다.

반면 실행 중인 컨테이너에 다음처럼 들어갔다가 나오는 경우:

```bash
docker exec -it ubuntu-container bash
```

이 셸은 추가 프로세스다. 여기서 `exit`해도 원래 주 프로세스가 살아 있다면 컨테이너는 계속 실행된다.

### 3-7. `attach`와 `exec`

| `docker attach` | `docker exec` |
|---|---|
| 컨테이너의 기존 주 프로세스 입출력에 연결 | 실행 중 컨테이너에 새 프로세스를 실행 |
| `exit`가 주 프로세스를 종료할 수 있음 | 추가 셸에서 `exit`해도 주 프로세스는 보통 유지 |
| 주 프로세스를 직접 관찰할 때 사용 | 점검·디버깅 명령 실행에 주로 사용 |

핵심 답안:

> `attach`는 기존 주 프로세스에 연결하고, `exec`는 실행 중인 컨테이너 안에 별도의 프로세스를 추가한다.

---

## 4. Dockerfile과 커스텀 이미지

이 과제의 핵심 예:

```dockerfile
FROM nginx:alpine

COPY site/index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

### 4-1. 명령별 의미

| 명령 | 의미 |
|---|---|
| `FROM nginx:alpine` | Nginx가 설치된 경량 Alpine 기반 이미지를 베이스로 선택 |
| `COPY ...` | 호스트의 정적 HTML을 이미지 내부 Nginx 기본 문서 경로로 복사 |
| `EXPOSE 80` | 컨테이너의 서비스 예정 포트가 80임을 문서화 |

커스텀 포인트는 기본 Nginx 페이지를 직접 만든 `index.html`로 교체한 것이다.

### 4-2. 빌드 컨텍스트

```bash
cd mandatory
docker build -t first-built-image .
```

- `-t first-built-image`: 이미지 이름 또는 태그 지정
- 마지막 `.`: 현재 디렉토리를 빌드 컨텍스트로 전달
- Docker는 컨텍스트 안의 파일만 `COPY`할 수 있다.
- Dockerfile의 `COPY site/index.html ...`이 성공하려면 빌드 컨텍스트 안에 `site/index.html`이 있어야 한다.

### 4-3. 빌드와 실행

```bash
docker build -t first-built-image .
docker run -d --name first-nginx-container -p 8080:80 first-built-image
docker ps
curl -i http://localhost:8080
docker logs first-nginx-container
```

이름을 구분한다.

- `first-built-image`: 이미지 이름
- `first-nginx-container`: 실행 컨테이너 이름

---

## 5. 포트 매핑

컨테이너는 호스트와 격리된 네트워크 공간에서 동작한다. 컨테이너 안의 Nginx가 80번 포트에서 대기하더라도, 호스트 브라우저가 그 포트에 자동으로 접근할 수 있는 것은 아니다.

```bash
docker run -d -p 8080:80 first-built-image
```

```text
브라우저/curl
localhost:8080
      │
      │ -p 8080:80
      ▼
컨테이너의 Nginx:80
```

형식:

```text
-p <호스트 포트>:<컨테이너 포트>
```

모범 답안:

> 포트 매핑은 격리된 컨테이너 내부의 서비스 포트를 호스트 포트와 연결하여 외부에서 접근할 수 있게 한다. `-p 8080:80`은 호스트의 8080번 요청을 컨테이너의 80번 포트로 전달한다.

### `EXPOSE`와 `-p`의 차이

- `EXPOSE 80`: 이미지 메타데이터에 사용 예정 포트를 기록한다.
- `-p 8080:80`: 컨테이너 실행 시 실제 네트워크 연결을 만든다.
- 따라서 Dockerfile에 `EXPOSE 80`만 써서는 `localhost:8080`으로 접속할 수 없다.

### 접속 장애 확인 순서

```bash
docker ps -a
docker logs first-nginx-container
docker port first-nginx-container
curl -i http://localhost:8080
```

1. 컨테이너가 실행 중인지 확인한다.
2. 중지되었다면 로그로 원인을 확인한다.
3. 실제 포트 매핑을 확인한다.
4. HTTP 상태 코드와 응답을 확인한다.

---

## 6. 바인드 마운트와 Docker 볼륨

### 6-1. 컨테이너 저장 공간의 한계

컨테이너의 기본 쓰기 계층에 저장한 데이터는 해당 컨테이너에 종속된다. 컨테이너를 삭제하면 그 데이터도 함께 사라진다. 코드 변경을 즉시 반영하거나 데이터를 컨테이너 생명주기와 분리하려면 마운트를 사용한다.

### 6-2. 바인드 마운트

호스트의 특정 파일 또는 디렉토리를 컨테이너 경로에 직접 연결한다.

```bash
docker run -d \
  --name bind-nginx \
  -p 8081:80 \
  -v "$(pwd)/site/index.html:/usr/share/nginx/html/index.html:ro" \
  nginx:alpine
```

- 왼쪽: 호스트의 실제 경로
- 오른쪽: 컨테이너 내부 경로
- `:ro`: 컨테이너에서 읽기 전용
- 호스트 파일을 수정하면 컨테이너에서 바로 변경을 확인할 수 있다.

적합한 용도: 소스코드, 설정 파일, 개발 중 즉시 반영.

### 6-3. Docker 볼륨

Docker가 관리하는 별도 저장 공간이다.

```bash
docker volume create mydata

docker run -d --name vol-test \
  -v mydata:/data \
  ubuntu sleep infinity

docker exec vol-test sh -c 'echo hi > /data/hello.txt'
docker exec vol-test cat /data/hello.txt
docker rm -f vol-test

docker run -d --name vol-test2 \
  -v mydata:/data \
  ubuntu sleep infinity

docker exec vol-test2 cat /data/hello.txt
```

마지막 명령에서 `hi`가 출력되면 첫 번째 컨테이너가 삭제된 뒤에도 볼륨 데이터가 유지된 것이다.

### 6-4. 비교

| 바인드 마운트 | Docker 볼륨 |
|---|---|
| 호스트의 지정 경로를 직접 사용 | Docker가 저장 위치를 관리 |
| 호스트 파일을 직접 편집하기 쉬움 | 컨테이너 간 데이터 재사용·영속성에 적합 |
| 호스트 디렉토리 구조에 의존 | 호스트 경로 의존성이 상대적으로 낮음 |
| 개발 소스·설정 공유에 적합 | DB 데이터·영속 데이터에 적합 |

모범 답안:

> 바인드 마운트는 사용자가 지정한 호스트 경로를 컨테이너에 연결하므로 개발 중 파일 변경을 즉시 반영하기 좋다. Docker 볼륨은 Docker가 관리하는 저장 공간으로, 컨테이너를 삭제하고 새 컨테이너를 만들어도 같은 볼륨을 연결하면 데이터를 다시 사용할 수 있다.

주의:

- `docker rm`은 컨테이너 삭제 명령이다.
- `docker volume rm`은 볼륨 자체를 삭제하므로 영속 데이터도 제거된다.
- 볼륨 영속성 시험에서는 컨테이너만 삭제하고 볼륨은 삭제하지 않아야 한다.

---

## 7. Git과 GitHub

### 7-1. 역할 차이

| Git | GitHub |
|---|---|
| 분산 버전 관리 도구 | Git 저장소 호스팅·협업 플랫폼 |
| 로컬에서도 커밋과 이력 관리 가능 | 원격 백업, 공유, PR, 이슈, 리뷰 제공 |
| 인터넷 없이도 기본 기능 사용 가능 | 원격 통신에는 네트워크와 인증 필요 |

모범 답안:

> Git은 파일 변경 이력을 로컬에서 기록하고 관리하는 도구다. GitHub는 Git 저장소를 원격에 올려 다른 사람과 공유하고 협업할 수 있게 하는 서비스다.

### 7-2. 기본 설정과 흐름

```bash
git config --global user.name "NAME"
git config --global user.email "EMAIL"
git config --global init.defaultBranch main
git config --list

git status
git add .
git commit -m "Add workstation assignment"
git remote -v
git push -u origin main
```

흐름:

```text
작업 디렉토리 --git add--> 스테이징 영역 --git commit--> 로컬 저장소
                                                   │
                                                git push
                                                   ▼
                                             GitHub 원격 저장소
```

### 7-3. 보안

README, 로그, 스크린샷에 다음을 포함하면 안 된다.

- 비밀번호
- GitHub 토큰
- 개인키
- 인증 코드
- 쿠키나 세션 정보

`git config --list`는 자격 증명 값이나 불필요한 개인정보가 출력되는지 확인한 후 필요한 부분만 기록한다. 비밀값이 Git 이력에 커밋되었다면 파일에서 지우는 것만으로 충분하지 않다. 이력을 정리하고 해당 비밀을 즉시 폐기·재발급해야 한다.

---

## 8. Docker Compose 보너스 범위

Compose는 긴 `docker run` 설정을 YAML 파일로 문서화하고 여러 서비스를 함께 관리하게 해 준다.

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./site:/usr/share/nginx/html:ro
```

필수 명령:

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

- `up -d`: 서비스 생성 및 백그라운드 실행
- `ps`: Compose 서비스 상태 확인
- `logs`: 서비스 로그 확인
- `down`: Compose로 만든 컨테이너와 기본 네트워크 정리
- Compose 네트워크 안에서는 서비스 이름을 호스트명처럼 사용할 수 있다.
- 환경 변수는 코드와 환경별 설정을 분리하는 데 사용한다.

---

## 9. 예상 단답형 문제와 정답

### 문제 1

현재 작업 디렉토리를 확인하는 명령은?

**정답:** `pwd`

### 문제 2

숨김 파일을 포함해 상세 목록을 확인하는 명령은?

**정답:** `ls -la`

### 문제 3

`chmod 755 app`에서 소유자, 그룹, 기타 사용자의 권한은?

**정답:** 소유자는 `rwx`, 그룹은 `r-x`, 기타 사용자는 `r-x`.

### 문제 4

디렉토리의 `x` 권한은 무엇을 의미하는가?

**정답:** 디렉토리에 진입하고 내부 항목의 경로에 접근할 수 있는 권한이다.

### 문제 5

Docker 이미지와 컨테이너의 차이는?

**정답:** 이미지는 실행 환경을 담은 템플릿이고, 컨테이너는 이미지로 생성한 실행 인스턴스다.

### 문제 6

`docker ps`와 `docker ps -a`의 차이는?

**정답:** `docker ps`는 실행 중인 컨테이너만, `docker ps -a`는 중지된 컨테이너를 포함해 모두 표시한다.

### 문제 7

`docker build -t my-web .`에서 마지막 `.`의 의미는?

**정답:** 현재 디렉토리를 Docker 빌드 컨텍스트로 사용한다는 뜻이다.

### 문제 8

`-p 8080:80`의 왼쪽과 오른쪽은 각각 무엇인가?

**정답:** 왼쪽 8080은 호스트 포트, 오른쪽 80은 컨테이너 포트다.

### 문제 9

Dockerfile의 `EXPOSE 80`만으로 호스트에서 접속할 수 있는가?

**정답:** 아니다. `EXPOSE`는 포트를 문서화할 뿐이며, 실행 시 `-p` 또는 동등한 포트 게시 설정이 필요하다.

### 문제 10

컨테이너 로그를 확인하는 명령은?

**정답:** `docker logs <컨테이너 이름>`

### 문제 11

`docker attach`와 `docker exec`의 차이는?

**정답:** `attach`는 기존 주 프로세스에 연결하고, `exec`는 실행 중인 컨테이너에서 새 프로세스를 실행한다.

### 문제 12

컨테이너를 삭제한 뒤에도 데이터를 유지하려면 무엇을 사용하는가?

**정답:** Docker 볼륨 또는 요구에 맞는 외부 마운트를 사용한다. 일반적인 영속 데이터에는 Docker 볼륨이 적합하다.

### 문제 13

바인드 마운트와 볼륨의 가장 큰 차이는?

**정답:** 바인드 마운트는 사용자가 지정한 호스트 경로를 직접 사용하고, 볼륨은 Docker가 저장 위치를 관리한다.

### 문제 14

Docker CLI 설치뿐 아니라 엔진 동작 여부까지 확인하는 명령은?

**정답:** `docker info`를 실행해 `Server` 정보가 정상 출력되는지 확인한다.

### 문제 15

Git과 GitHub의 차이는?

**정답:** Git은 로컬 버전 관리 도구이고 GitHub는 Git 저장소를 원격에서 공유하고 협업하는 플랫폼이다.

---

## 10. 예상 서술형 문제와 모범 답안

### 10-1. 포트 매핑이 필요한 이유를 설명하시오.

> Docker 컨테이너는 호스트와 격리된 네트워크 환경에서 실행된다. 따라서 컨테이너 내부 서비스가 80번 포트에서 대기하더라도 호스트에서 자동으로 접근할 수 없다. `-p 8080:80`처럼 호스트 포트와 컨테이너 포트를 매핑하면 호스트의 8080번 요청이 컨테이너의 80번 포트로 전달되어 브라우저나 `curl`로 서비스에 접근할 수 있다.

### 10-2. Docker 볼륨의 영속성을 검증하는 방법을 설명하시오.

> 먼저 볼륨을 생성하고 첫 번째 컨테이너의 특정 경로에 연결한다. 연결된 경로에 파일을 쓴 뒤 내용을 확인한다. 그다음 컨테이너만 삭제하고 같은 볼륨을 새 컨테이너에 연결한다. 새 컨테이너에서 기존 파일이 그대로 읽히면 데이터가 컨테이너가 아닌 볼륨에 저장되어 영속성이 유지된 것이다.

### 10-3. 재현 가능한 개발 환경에서 Dockerfile이 하는 역할을 설명하시오.

> Dockerfile은 베이스 이미지, 파일 복사, 패키지 설치, 환경 설정 등 이미지 생성 절차를 코드로 기록한 설계도다. 같은 Dockerfile과 빌드 컨텍스트를 사용하면 여러 개발자가 유사한 실행 환경을 반복해서 만들 수 있으므로 수동 설치 차이와 환경 불일치를 줄일 수 있다.

### 10-4. `644` 파일과 `755` 디렉토리가 흔히 사용되는 이유를 설명하시오.

> 일반 문서 파일은 소유자만 수정하고 다른 사용자는 읽기만 가능하면 되는 경우가 많으므로 `644`가 적합하다. 디렉토리는 내부 파일에 접근하려면 실행 권한이 필요하므로 소유자는 읽기·쓰기·진입이 가능한 `rwx`, 나머지는 읽기·진입이 가능한 `r-x`를 주는 `755`가 흔히 사용된다.

### 10-5. 기술 문서에 명령과 출력 결과를 함께 기록해야 하는 이유는?

> 명령만 기록하면 실제 성공 여부를 알 수 없고, 출력만 기록하면 어떤 절차로 결과를 얻었는지 재현하기 어렵다. 명령과 결과를 함께 남기면 수행 여부, 성공 상태, 오류 원인을 검증할 수 있고 평가자도 같은 절차를 따라 재현할 수 있다.

---

## 11. 상황형 문제

### 상황 1

`docker --version`은 성공하지만 `docker run hello-world`가 실패한다.

**판단:** CLI는 설치되었지만 Docker 엔진이 실행되지 않았거나 CLI가 엔진에 연결되지 않았을 수 있다.

**확인:** `docker info`를 실행하고 OrbStack 또는 Docker Desktop의 실행 상태를 확인한다.

### 상황 2

Nginx 컨테이너가 실행 직후 종료되었다.

**정답 순서:**

```bash
docker ps -a
docker logs <컨테이너 이름>
```

컨테이너를 바로 삭제하지 말고 상태와 로그를 먼저 확인해 원인을 보존한다.

### 상황 3

Dockerfile에 `EXPOSE 80`을 썼지만 `localhost:8080` 접속이 안 된다.

**원인:** 실제 포트 게시가 되지 않았을 가능성이 크다.

**해결:** 컨테이너를 `-p 8080:80`으로 실행하고 `docker ps`, `docker port`, `curl`로 확인한다.

### 상황 4

호스트의 HTML을 고쳤는데 이미 빌드한 컨테이너 화면은 바뀌지 않는다.

**이유:** `COPY`된 파일은 이미지 빌드 시점의 사본이다.

**선택지:**

- 새 내용을 이미지에 포함하려면 이미지를 다시 빌드하고 컨테이너를 재생성한다.
- 개발 중 즉시 반영하려면 바인드 마운트를 사용한다.

### 상황 5

볼륨에 파일을 쓴 뒤 컨테이너를 삭제했는데 새 컨테이너에서 파일이 안 보인다.

**확인할 것:**

1. 새 컨테이너에 같은 이름의 볼륨을 연결했는가?
2. 두 컨테이너에서 볼륨을 같은 내부 경로에 연결했는가?
3. 컨테이너를 지울 때 볼륨 자체도 함께 삭제하지 않았는가?
4. 파일을 실제로 마운트 경로 안에 썼는가?

### 상황 6

`docker exec ubuntu-container2 pwd`가 `No such container`를 출력한다.

**확인:** `docker ps -a --format '{{.Names}}'`로 실제 컨테이너 이름을 확인한다. 이름 오타나 하이픈 누락을 고친다.

---

## 12. 실전 명령 흐름 암기

### Docker 상태 점검

```bash
docker --version
docker info
docker images
docker ps -a
```

### 커스텀 웹 이미지

```bash
cd mandatory
docker build -t first-built-image .
docker images first-built-image
docker run -d --name first-nginx-container -p 8080:80 first-built-image
docker ps
docker logs first-nginx-container
curl -i http://localhost:8080
```

### 장애 진단

```bash
docker ps -a
docker logs <container>
docker inspect <container>
docker port <container>
```

### 볼륨 영속성

```bash
docker volume create mydata
docker run -d --name vol1 -v mydata:/data ubuntu sleep infinity
docker exec vol1 sh -c 'echo hi > /data/hello.txt'
docker rm -f vol1
docker run -d --name vol2 -v mydata:/data ubuntu sleep infinity
docker exec vol2 cat /data/hello.txt
```

---

## 13. 마지막 10분 체크리스트

- [ ] 절대 경로와 상대 경로를 예시로 설명할 수 있다.
- [ ] `pwd`, `ls -la`, `cd`, `mkdir`, `touch`, `cat`, `cp`, `mv`, `rm`을 설명할 수 있다.
- [ ] `r=4`, `w=2`, `x=1`로 `755`와 `644`를 계산할 수 있다.
- [ ] 파일과 디렉토리에서 `x`의 의미가 다름을 설명할 수 있다.
- [ ] 이미지, 컨테이너, Dockerfile의 관계를 설명할 수 있다.
- [ ] `docker run`, `start`, `exec`, `attach`의 차이를 말할 수 있다.
- [ ] `docker ps`와 `docker ps -a`의 차이를 말할 수 있다.
- [ ] `EXPOSE 80`과 `-p 8080:80`의 차이를 말할 수 있다.
- [ ] 바인드 마운트와 볼륨을 비교할 수 있다.
- [ ] 컨테이너 삭제 전후의 볼륨 영속성 검증 절차를 말할 수 있다.
- [ ] Git과 GitHub의 차이를 한 문장으로 설명할 수 있다.
- [ ] 실패한 컨테이너를 삭제하기 전에 `docker logs`를 확인해야 함을 안다.
- [ ] 로그와 스크린샷에서 토큰·비밀번호·개인키를 제거해야 함을 안다.

## 한 줄 최종 암기

> **Dockerfile로 이미지를 만들고, 이미지로 컨테이너를 실행하며, 포트로 서비스에 연결하고, 마운트와 볼륨으로 파일과 데이터를 컨테이너 생명주기 밖에 둔다. Git은 그 과정을 버전 관리하고 GitHub는 이를 원격에서 공유한다.**
