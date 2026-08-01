# hello-world 및 Docker 기본 운영 기록 방식 비교

## 1. dubu-alt 저장소

### 진행 순서

`E1-1/README.md`에서 다음 순서로 진행했다.

1. `docker --version`
2. `docker info | head -20`
3. `docker run hello-world`
4. `docker run -it ubuntu bash`
5. Ubuntu 내부에서 `ls -la`, `echo`, `cat /etc/os-release`
6. `docker images`
7. `docker ps -a`
8. `docker ps`

체크리스트에는 다음 Docker 운영 항목을 모두 완료로 표시했다.

- `docker pull ubuntu`
- `docker images`
- `docker run`
- `docker stop`
- `docker ps`, `docker ps -a`
- `docker logs`
- `docker stats`

### hello-world 기록

다음 핵심 출력을 기록했다.

```console
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.(amd64)
 ...

→ 성공
```

전체 안내문을 모두 붙이지 않고 Docker Client, 데몬, 이미지 다운로드가 확인되는 부분을 남겼다.

### 이미지와 컨테이너 목록 기록

`docker images`, `docker ps -a`, `docker ps`의 예시 출력을 각각 기록했다.

- 이미지 목록에는 커스텀 웹 서버, Ubuntu, hello-world가 함께 표시됐다.
- 전체 컨테이너 목록에는 종료된 hello-world와 Ubuntu가 표시됐다.
- 실행 중인 컨테이너 목록에는 웹 서버 컨테이너가 표시됐다.

### Ubuntu 기록

```bash
docker run -it ubuntu bash
```

컨테이너 내부에서 다음을 실행했다.

```bash
ls -la
echo "hello"
cat /etc/os-release
exit
```

Ubuntu 내부 파일 구조와 운영체제 정보를 실제 출력으로 기록했다.

### 평가

장점:

- hello-world의 성공 근거를 실제 출력으로 남겼다.
- Ubuntu 컨테이너 내부 진입 결과가 명확하다.
- `docker images`, `docker ps`, `docker ps -a`를 구분해 기록했다.

보완할 점:

- 일부 이미지 ID, 컨테이너 ID, 크기와 시간이 실제 결과라기보다 예시처럼 보인다.
- 체크리스트에는 `docker stop`, `docker logs`, `docker stats`를 완료했다고 했지만 해당 수행 출력은 찾기 어렵다.
- 명령 수행 기록과 체크리스트 사이의 증거 대응이 불분명하다.
- 같은 내용이 별도 `final_checklist.md`에도 반복된다.

## 2. jhkr1 저장소

### 진행 순서

README에서 Docker 운영, hello-world, Ubuntu를 서로 다른 설명 섹션으로 나눴다.

1. `docker images`
2. `docker ps`
3. `docker ps -a`
4. `docker stats --no-stream`
5. `docker run hello-world`
6. `docker run -it ubuntu bash`
7. Ubuntu 내부에서 `echo`
8. 이후 볼륨 단계에서 `docker exec`
9. 웹 서버 단계에서 `docker logs`

### Docker 운영 기록

```bash
docker images
docker ps
docker ps -a
docker stats --no-stream
```

명령 아래에 이미지와 컨테이너 상태를 축약한 표 형태의 출력을 적고 각 명령의 역할을 설명했다.

- `docker images`: 로컬 이미지 확인
- `docker ps`: 실행 중인 컨테이너 확인
- `docker ps -a`: 종료된 컨테이너까지 확인
- `docker stats --no-stream`: 자원 사용량을 한 번 출력

### hello-world 기록

```console
$ docker run hello-world
Hello from Docker!
```

출력은 한 줄만 남기고 다음 네 가지를 검증한다고 설명했다.

- 이미지 다운로드
- 컨테이너 생성
- 컨테이너 실행과 출력
- CLI와 Docker Engine 연결

### Ubuntu 기록

```bash
docker run -it ubuntu bash
echo "inside container"
exit
```

`-i`, `-t`, 이미지 이름, 실행 명령의 의미를 각각 설명했다. 컨테이너는 메인 프로세스가 종료되면 함께 종료된다는 점도 설명했다.

### attach와 exec

뒤쪽의 별도 섹션에서 두 명령을 비교했다.

- `docker attach`: 컨테이너의 메인 프로세스에 직접 연결
- `docker exec`: 실행 중인 컨테이너 안에 새 프로세스를 생성
- `attach`에서 `exit` 또는 `Ctrl+C`를 사용하면 메인 프로세스와 컨테이너가 종료될 수 있음
- `exec`에서 나가면 새로 만든 프로세스만 종료되고 컨테이너는 유지됨

실제 활용 사례로 볼륨 컨테이너에 `docker exec`로 접속해 데이터를 작성하고 확인했다.

### 로그 기록

Nginx 웹 서버 단계에서 다음 명령을 사용했다.

```bash
docker logs mission-web-8080
```

로그를 요청 확인, 오류 분석, 즉시 종료 원인 파악에 사용한다고 설명했다.

### 평가

장점:

- 명령의 의미와 사용하는 상황이 잘 설명돼 있다.
- hello-world를 단순 출력이 아니라 네 단계의 검증 과정으로 해석했다.
- `attach`와 `exec`를 컨테이너 생명주기와 연결했다.
- 로그 확인을 실제 웹 서버 단계에 배치했다.

보완할 점:

- 실제 명령 출력보다 설명이 훨씬 많다.
- Docker 운영 목록의 출력이 실제 수행 결과인지 요약 예시인지 구분하기 어렵다.
- hello-world는 실제 출력이 `Hello from Docker!` 한 줄뿐이다.
- 일부 체크 항목은 설명만 있고 실제 수행 증거가 부족하다.

## 3. 두 저장소 비교

| 항목 | dubu-alt | jhkr1 |
|---|---|---|
| hello-world | 핵심 출력 일부 기록 | 한 줄 출력과 의미 설명 |
| 이미지 목록 | 상세 표 기록 | 명령과 요약 상태 기록 |
| `docker ps`/`ps -a` | 각각 실제 형식으로 기록 | 차이와 사용 목적 설명 |
| Ubuntu | 내부 명령과 출력 기록 | 간단한 명령과 옵션 설명 |
| `attach`/`exec` | 실습 기록이 불분명 | 별도 비교 섹션으로 설명 |
| `docker logs` | 체크했지만 증거가 부족 | Nginx 단계에서 사용 |
| `docker stats` | 체크했지만 증거가 부족 | 명령과 의미 기록 |
| 문서 분량 | 출력과 예시가 많음 | 설명이 매우 많음 |

## 4. 우리 저장소에 적용할 방식

### hello-world

실제로 출력된 내용 중 다음을 기록한다.

- 이미지가 로컬에 없어 Docker Hub에서 다운로드한 과정
- `Hello from Docker!`
- 이미지 목록
- 종료 코드가 `Exited (0)`인 컨테이너 목록

이렇게 하면 별도의 긴 설명 없이 다운로드, 생성, 실행, 정상 종료를 실제 결과로 확인할 수 있다.

### `docker images`, `docker ps`, `docker ps -a`

실제 출력값을 그대로 사용하되 다음 차이만 짧게 설명한다.

- 이미지는 컨테이너를 만들기 위한 실행 환경이다.
- `docker ps`는 실행 중인 컨테이너만 표시한다.
- `docker ps -a`는 종료된 컨테이너도 표시한다.
- `Exited (0)`은 오류 없이 종료됐다는 뜻이다.

### Ubuntu

다음 단계에서 실제 컨테이너를 실행한 뒤 내부 명령과 출력을 기록한다.

```bash
docker pull ubuntu
docker run -dit --name codyssey-ubuntu ubuntu bash
docker exec codyssey-ubuntu ls
docker exec codyssey-ubuntu sh -c 'echo "Hello from Ubuntu container"'
```

### attach와 exec

설명만 적지 않고 동일한 Ubuntu 컨테이너에서 직접 관찰한다.

- `attach`로 메인 프로세스에 연결
- 안전하게 분리해 컨테이너가 계속 실행되는지 확인
- `exec`로 별도 명령을 실행
- `exec`가 끝나도 컨테이너가 계속 실행되는지 확인

### logs와 stats

- `docker stats --no-stream`은 실행 중인 Ubuntu 또는 Nginx 컨테이너에서 확인한다.
- `docker logs`는 실제 요청 로그가 남는 Nginx 컨테이너에서 확인한다.

Ubuntu에서 의미 없는 빈 로그를 억지로 기록하지 않는다.

## 5. 결론

우리 방식은 dubu-alt처럼 실제 출력으로 성공을 증명하되, jhkr1처럼 각 명령을 사용하는 이유를 필요한 만큼만 설명한다.

현재 hello-world 기록은 다음 사항을 실제 결과로 모두 확인했으므로 충분하다.

- 이미지 다운로드 성공
- 이미지 목록 확인
- 컨테이너 생성 및 실행
- 컨테이너 정상 종료
- 실행 중인 컨테이너와 종료된 컨테이너 목록의 차이

다음 단계는 Ubuntu 이미지를 내려받고 실행 중인 컨테이너를 만들어 `exec`, `stats`, `stop`을 실제로 확인하는 것이다.
