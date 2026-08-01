# 개발 워크스테이션 시험 치트시트

> `instruction.md` 핵심 압축본 — 시험 직전 빠르게 반복하기

## 1. 무조건 외울 핵심

- 절대 경로: `/`부터 시작하는 전체 경로
- 상대 경로: 현재 위치를 기준으로 한 경로
- 권한 숫자: `r=4`, `w=2`, `x=1`
- `755 = rwxr-xr-x`, `644 = rw-r--r--`
- 이미지: 컨테이너를 만드는 템플릿
- 컨테이너: 이미지로 만든 실행 인스턴스
- Dockerfile: 이미지를 만드는 설계도
- `EXPOSE`: 포트 문서화
- `-p`: 실제 포트 연결
- 바인드 마운트: 호스트 경로 직접 연결
- 볼륨: Docker가 관리하는 영속 저장 공간
- Git: 로컬 버전 관리
- GitHub: 원격 저장소·협업 플랫폼

---

## 2. 터미널 필수 명령

| 목적 | 명령 |
|---|---|
| 현재 위치 | `pwd` |
| 숨김 파일 포함 상세 목록 | `ls -la` |
| 디렉토리 이동 | `cd <directory>` |
| 상위 디렉토리 이동 | `cd ..` |
| 디렉토리 생성 | `mkdir <directory>` |
| 중간 경로까지 생성 | `mkdir -p a/b` |
| 빈 파일 생성 | `touch <file>` |
| 파일 내용 확인 | `cat <file>` |
| 파일 복사 | `cp <source> <destination>` |
| 이동·이름 변경 | `mv <source> <destination>` |
| 파일 삭제 | `rm <file>` |
| 빈 디렉토리 삭제 | `rmdir <directory>` |

경로 기호:

```text
/    루트
.    현재 디렉토리
..   상위 디렉토리
~    사용자 홈
```

---

## 3. 권한

```text
-rwxr-xr-x
│└─┬─┘└─┬─┘└─┬─┘
│ 소유자 그룹 기타
└ -: 일반 파일, d: 디렉토리
```

| 권한 | 숫자 | 파일 | 디렉토리 |
|---|---:|---|---|
| `r` | 4 | 내용 읽기 | 목록 보기 |
| `w` | 2 | 내용 수정 | 항목 생성·삭제 |
| `x` | 1 | 파일 실행 | 진입·내부 경로 접근 |

```bash
ls -l file.txt        # 파일 권한 확인
ls -ld directory      # 디렉토리 자체 권한 확인
chmod 644 file.txt
chmod 755 directory
chmod 600 secret.txt
```

암기:

```text
7 = rwx = 4+2+1
6 = rw- = 4+2
5 = r-x = 4+1
4 = r--
```

---

## 4. Docker 핵심 구조

```text
Dockerfile ──docker build──▶ 이미지 ──docker run──▶ 컨테이너
   설계도                       템플릿                 실행 인스턴스
```

| 구분 | 핵심 |
|---|---|
| 이미지 | 실행 환경을 담은 템플릿 |
| 컨테이너 | 이미지로 만든 실행 프로세스 |
| Dockerfile | 이미지 생성 절차를 기록한 파일 |

Docker의 목적:

> 애플리케이션과 실행 환경을 함께 묶어 환경 차이를 줄이고, 재현 가능한 격리 환경을 제공한다.

---

## 5. Docker 필수 명령

### 설치·엔진 확인

```bash
docker --version     # CLI 설치 확인
docker info          # Docker 엔진 연결 확인
```

`docker --version`만 성공해도 컨테이너가 실행된다는 뜻은 아니다.  
`docker info`에 `Server` 정보가 출력되어야 한다.

### 이미지

~~`docker pull ubuntu`~~

```bash
docker images
docker rmi <image>
```

### 컨테이너

```bash
docker run <image>           # 새 컨테이너 생성 + 실행
docker ps                    # 실행 중인 컨테이너
docker ps -a                 # 중지된 것까지 전체
docker stop <container>
docker start <container>     # 기존 컨테이너 다시 실행
docker rm <container>
docker logs <container>
docker stats --no-stream <container>
```

### 컨테이너 내부 접근

```bash
docker exec -it <container> sh
docker attach <container>
```

| `exec` | `attach` |
|---|---|
| 새 프로세스를 실행 | 기존 주 프로세스에 연결 |
| 셸에서 나와도 주 컨테이너는 보통 유지 | `exit`가 주 프로세스를 끝낼 수 있음 |

컨테이너는 주 프로세스(PID 1)가 종료되면 중지된다.

---

## 6. Dockerfile

```dockerfile
FROM nginx:alpine

COPY site/index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

| 명령 | 의미 |
|---|---|
| `FROM` | 베이스 이미지 선택 |
| `COPY` | 호스트 파일을 이미지 안으로 복사 |
| `EXPOSE` | 컨테이너의 사용 예정 포트 문서화 |

빌드:

```bash
cd mandatory
docker build -t first-built-image .
```

- `-t first-built-image`: 이미지 이름 지정
- 마지막 `.`: 현재 디렉토리가 빌드 컨텍스트
- `COPY`할 파일은 빌드 컨텍스트 안에 있어야 함

---

## 7. 포트 매핑

```bash
docker run -d \
  --name first-nginx-container \
  -p 8080:80 \
  first-built-image
```

```text
-p <호스트 포트>:<컨테이너 포트>

localhost:8080 ──▶ container:80
```

핵심:

| `EXPOSE 80` | `-p 8080:80` |
|---|---|
| 포트 사용 예정 문서화 | 실제 네트워크 연결 |
| 접속 경로를 만들지 않음 | 호스트에서 컨테이너 서비스에 접근 가능 |

모범 답안:

> 컨테이너는 격리된 네트워크에서 실행되므로, 호스트에서 내부 서비스에 접근하려면 호스트 포트와 컨테이너 포트를 매핑해야 한다.

접속 확인:

```bash
docker ps
docker port first-nginx-container
curl -i http://localhost:8080
docker logs first-nginx-container
```

---

## 8. 마운트와 볼륨

| 바인드 마운트 | Docker 볼륨 |
|---|---|
| 호스트 경로를 직접 연결 | Docker가 저장 위치 관리 |
| 호스트 변경 즉시 반영 | 컨테이너 삭제 후에도 데이터 유지 |
| 소스·설정 파일에 적합 | DB·영속 데이터에 적합 |
| 호스트 경로에 의존 | 경로 의존성이 상대적으로 낮음 |

### 바인드 마운트

```bash
docker run -d \
  -p 8081:80 \
  -v "$(pwd)/site:/usr/share/nginx/html:ro" \
  nginx:alpine
```

```text
-v <호스트 경로>:<컨테이너 경로>
:ro = 컨테이너에서 읽기 전용
```

### 볼륨 영속성 검증

```bash
docker volume create mydata

docker run -d --name vol1 \
  -v mydata:/data ubuntu sleep infinity

docker exec vol1 sh -c 'echo hi > /data/hello.txt'
docker rm -f vol1

docker run -d --name vol2 \
  -v mydata:/data ubuntu sleep infinity

docker exec vol2 cat /data/hello.txt
```

`hi`가 출력되면 컨테이너 삭제 후에도 볼륨 데이터가 유지된 것이다.

주의:

- `docker rm`: 컨테이너 삭제
- `docker volume rm`: 볼륨과 영속 데이터 삭제

---

## 9. Git과 GitHub

| Git | GitHub |
|---|---|
| 로컬 버전 관리 도구 | 원격 저장소·협업 서비스 |
| 변경 이력과 커밋 관리 | 공유, 백업, PR, 이슈, 리뷰 |
| 인터넷 없이 기본 기능 사용 가능 | 원격 작업에 네트워크·인증 필요 |

```text
작업 디렉토리 ─git add─▶ 스테이징 ─git commit─▶ 로컬 저장소
                                                     │
                                                  git push
                                                     ▼
                                               GitHub 원격
```

```bash
git config --global user.name "NAME"
git config --global user.email "EMAIL"
git config --global init.defaultBranch main
git config --list

git status
git add .
git commit -m "message"
git remote -v
git push -u origin main
```

보안:

- 토큰, 비밀번호, 개인키, 인증 코드 커밋 금지
- 로그와 스크린샷의 민감정보 마스킹
- 유출 시 이력 정리뿐 아니라 비밀값 폐기·재발급

---

## 10. 장애 진단 공식

실패한 컨테이너는 바로 삭제하지 않는다.

```bash
docker ps -a
docker logs <container>
docker inspect <container>
docker port <container>
curl -i http://localhost:<port>
```

순서:

```text
상태 확인 → 로그 확인 → 설정 확인 → 수정 → 재실행 → 결과 검증
```

자주 나오는 문제:

| 증상 | 원인·확인 |
|---|---|
| `No such container` | `docker ps -a`로 실제 이름 확인 |
| 컨테이너 즉시 종료 | 주 프로세스 종료 또는 실행 오류, `docker logs` 확인 |
| `localhost` 접속 실패 | 실행 상태와 `-p` 포트 매핑 확인 |
| HTML 수정이 반영 안 됨 | `COPY`는 빌드 시점 사본, 재빌드 또는 바인드 마운트 |
| 새 컨테이너에서 데이터 없음 | 같은 볼륨·같은 마운트 경로인지 확인 |

---

## 11. 시험 예상 질문 한 줄 답안

1. **절대 경로와 상대 경로의 차이?**  
   절대 경로는 `/`부터 시작하며 현재 위치와 무관하고, 상대 경로는 현재 위치를 기준으로 해석된다.

2. **`755`의 의미?**  
   소유자는 `rwx`, 그룹과 기타 사용자는 `r-x` 권한을 가진다.

3. **디렉토리의 `x` 권한?**  
   디렉토리에 진입하고 내부 경로에 접근하는 권한이다.

4. **이미지와 컨테이너의 차이?**  
   이미지는 템플릿이고 컨테이너는 이미지로 만든 실행 인스턴스다.

5. **`docker ps`와 `docker ps -a`의 차이?**  
   전자는 실행 중인 컨테이너만, 후자는 중지된 컨테이너까지 표시한다.

6. **`docker run`과 `docker start`의 차이?**  
   `run`은 이미지에서 새 컨테이너를 생성·실행하고, `start`는 기존 컨테이너를 다시 실행한다.

7. **빌드 명령의 마지막 `.`은?**  
   현재 디렉토리를 빌드 컨텍스트로 사용한다는 뜻이다.

8. **`-p 8080:80`의 의미?**  
   호스트 8080번 포트를 컨테이너 80번 포트에 연결한다.

9. **`EXPOSE`만으로 접속 가능한가?**  
   아니다. 실제 연결에는 실행 시 `-p` 같은 포트 게시 설정이 필요하다.

10. **바인드 마운트와 볼륨의 차이?**  
    바인드 마운트는 호스트 경로를 직접 사용하고, 볼륨은 Docker가 저장 위치를 관리한다.

11. **볼륨 영속성을 어떻게 증명하는가?**  
    볼륨에 데이터를 기록하고 컨테이너를 삭제한 뒤, 같은 볼륨을 새 컨테이너에 연결해 데이터를 다시 읽는다.

12. **Git과 GitHub의 차이?**  
    Git은 로컬 버전 관리 도구이고 GitHub는 Git 저장소를 원격에서 공유·협업하는 플랫폼이다.

---

## 12. 최종 암기 명령

```bash
# 환경 확인
pwd
ls -la
docker --version
docker info

# 이미지 빌드와 웹 서버 실행
cd mandatory
docker build -t first-built-image .
docker run -d --name first-nginx-container -p 8080:80 first-built-image

# 검증
docker ps
docker logs first-nginx-container
curl -i http://localhost:8080

# 상태 전체 확인
docker images
docker ps -a
docker stats --no-stream first-nginx-container
```

## 최종 한 문장

> Dockerfile로 이미지를 만들고, 이미지로 컨테이너를 실행하며, 포트로 서비스에 연결하고, 바인드 마운트와 볼륨으로 파일과 데이터를 외부에 유지한다. Git은 변경 이력을 관리하고 GitHub는 이를 원격에서 공유한다.
