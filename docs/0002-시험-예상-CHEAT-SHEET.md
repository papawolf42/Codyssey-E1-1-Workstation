# 0002. 시험 예상 CHEAT SHEET

> **공식 기술 범위의 유일한 근거:** `instruction.md`
> 아래는 학습 목표·필수 실습 기반 예상이며 실제 시험 문항은 아니다.
> 시험 형식·문항 수·배점·제한 시간은 `instruction.md`에 없다.
> 당일 운영 정보: [0005 시험 당일 운영 주의사항](./0005-시험-당일-운영-주의사항.md)

## 1. 최우선 6개

`instruction.md:68-75`

1. 절대 경로와 상대 경로
2. 권한 `r/w/x`, `755`, `644`
3. Dockerfile과 커스텀 이미지
4. 포트 매핑이 필요한 이유
5. Docker 볼륨과 영속성
6. Git과 GitHub의 차이

Compose·환경 변수·SSH 키는 선택 보너스다. 예시에 나온 특정 OS·버전·포트·이름·출력은 고정 요구가 아니다.

---

## 2. 한 줄 답

| 개념 | 답 |
|---|---|
| 절대 경로 | 루트 `/`부터 시작하며 현재 위치와 무관 |
| 상대 경로 | 현재 작업 디렉터리 기준 |
| 권한 숫자 | `r=4`, `w=2`, `x=1` |
| `755` | `rwxr-xr-x` |
| `644` | `rw-r--r--` |
| 디렉터리 `x` | 진입·내부 경로 탐색 |
| 이미지 | 컨테이너를 만드는 읽기 전용 템플릿 |
| 컨테이너 | 이미지로 만든 실행 인스턴스 |
| Dockerfile | 이미지 빌드 과정을 기록한 명령 정의서 |
| `-p H:C` | 호스트 `H` → 컨테이너 `C` |
| `EXPOSE` | 사용 포트 설명; 실제 전달 규칙은 아님 |
| 바인드 마운트 | 지정한 호스트 경로를 직접 연결 |
| Docker 볼륨 | Docker가 관리하는 영속 저장소 |
| `attach` | 기존 메인 프로세스 입출력에 연결 |
| `exec` | 실행 중 컨테이너에서 새 프로세스 실행 |
| Git | 로컬 버전 관리 도구 |
| GitHub | Git 원격 저장소·협업 서비스 |
| 민감정보 | 토큰·비밀번호·개인키는 마스킹하고, 노출 시 제거·재발급 |

---

## 3. 바로 쓰는 예상 답

### 경로

> 절대 경로는 루트부터 전체 위치를 표현해 현재 위치와 무관하다. 상대 경로는 현재 작업 디렉터리를 기준으로 해석된다.

### 권한

> `r=4`, `w=2`, `x=1`을 소유자·그룹·기타 사용자 순서로 합산한다. `755`는 `rwxr-xr-x`, `644`는 `rw-r--r--`이다. 디렉터리의 `x`는 진입과 탐색 권한이다.

### 이미지·컨테이너·Dockerfile

> 이미지는 실행 환경을 담은 읽기 전용 템플릿이고, 컨테이너는 이미지로 만든 실행 인스턴스다. Dockerfile은 이미지를 재현 가능하게 빌드하는 과정을 기록한다.

### 포트 매핑

> 컨테이너 내부 서비스 포트는 호스트에 자동으로 연결되지 않는다. `-p <HOST_PORT>:<CONTAINER_PORT>`로 호스트 요청을 컨테이너 서비스에 전달한다.

### 바인드 마운트·볼륨

> 바인드 마운트는 지정한 호스트 경로를 직접 연결한다. 볼륨은 Docker가 관리하며 컨테이너를 삭제해도 볼륨을 삭제하지 않으면 데이터가 유지된다.

### 볼륨 영속성 검증

> 볼륨 생성 → 첫 컨테이너 연결 → 데이터 저장 → 컨테이너 삭제 → 새 컨테이너에 같은 볼륨 연결 → 기존 데이터 확인.

### `attach`·`exec`

> `attach`는 기존 메인 프로세스에 연결하고, `exec`는 실행 중인 컨테이너에서 별도의 새 프로세스를 실행한다.

### Git·GitHub

> Git은 로컬 변경 이력을 관리한다. GitHub는 Git 저장소를 원격에 보관하고 공유·협업하게 한다. `commit`은 로컬 이력, `push`는 원격 전송이다.

---

## 4. 명령 카드

```console
# 터미널·권한
pwd
ls -la
cd <DIRECTORY>
mkdir <DIRECTORY>
touch <FILE>
cat <FILE>
cp <SOURCE> <DESTINATION>
mv <SOURCE> <DESTINATION>
rm <FILE>
ls -l <FILE>
ls -ld <DIRECTORY>
chmod 644 <FILE>
chmod 755 <DIRECTORY>
```

```console
# Docker 점검·운영
docker --version
docker info
docker pull <IMAGE>
docker images
docker build -t <IMAGE>:<TAG> <BUILD_CONTEXT>
docker run <OPTIONS> <IMAGE>
docker ps
docker ps -a
docker stop <CONTAINER>
docker logs <CONTAINER>
docker stats --no-stream <CONTAINER>
docker attach <CONTAINER>
docker exec -it <CONTAINER> <SHELL>
```

```console
# 포트·마운트
docker run -p <HOST_PORT>:<CONTAINER_PORT> <IMAGE>
docker run --mount type=bind,src=<HOST_PATH>,dst=<CONTAINER_PATH> <IMAGE>
docker volume create <VOLUME>
docker run --mount type=volume,src=<VOLUME>,dst=<CONTAINER_PATH> <IMAGE>
```

```console
# Git
git config --list
git config user.name
git config user.email
git status
git add <FILE>
git commit -m "<MESSAGE>"
git remote -v
git push origin <BRANCH>
```

---

## 5. 마지막 비교

| A | B | 차이 |
|---|---|---|
| 절대 경로 | 상대 경로 | 루트 기준 / 현재 위치 기준 |
| 이미지 | 컨테이너 | 실행 템플릿 / 실행 인스턴스 |
| `build` | `run` | 이미지 생성 / 컨테이너 생성·실행 |
| `ps` | `ps -a` | 실행 중 / 종료 포함 전체 |
| `attach` | `exec` | 기존 프로세스 연결 / 새 프로세스 실행 |
| `EXPOSE` | `-p` | 포트 설명 / 실제 포트 전달 |
| 바인드 마운트 | 볼륨 | 호스트 경로 / Docker 관리 저장소 |
| Git | GitHub | 로컬 버전 관리 / 원격 저장·협업 |
| `commit` | `push` | 로컬 이력 / 원격 전송 |

## 6. 20초 체크

- [ ] `r=4`, `w=2`, `x=1`; `755`, `644`
- [ ] `-p`는 호스트:컨테이너
- [ ] 이미지·컨테이너·Dockerfile
- [ ] `ps`/`ps -a`, `attach`/`exec`
- [ ] 바인드 마운트/볼륨
- [ ] 볼륨 영속성 6단계
- [ ] Git/GitHub, `add`/`commit`/`push`
