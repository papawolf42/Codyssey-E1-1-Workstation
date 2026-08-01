# Docker 설치·점검 기록 방식 검토

## 1. 참고 저장소 비교

### dubu-alt 저장소

`E1-1/README.md`에서 Docker 설치와 점검을 체크리스트와 수행 기록으로 나누어 작성했다.

체크리스트에는 다음 항목이 있다.

- Docker 설치 완료
- Docker 버전 확인 — `docker --version`
- Docker 데몬 동작 확인 — `docker info`
- Docker 기본 명령 테스트 완료

수행 기록의 `4-2) Docker 검증`에는 다음과 같이 실제 명령과 출력 일부를 함께 적었다.

```console
$ docker --version
Docker version 28.5.2, build ecc6942

$ docker info | head -20
Client:
 Version:    28.5.2
 Context:    orbstack
```

별도의 `final_checklist.md`에도 `docker --version`, `docker info`와 `docker info` 출력 스크린샷을 다시 기록했다.

이 방식은 실행 결과가 있어 확인하기 쉽지만 같은 내용이 README와 별도 체크리스트에 중복된다. 또한 `docker info | head -20`은 Docker 플러그인 목록이 길면 Server 정보가 잘려 실제 데몬 연결 여부를 충분히 보여주지 못할 수 있다.

### jhkr1 저장소

`README.md`의 `7. Docker 설치 및 기본 점검`에서 다음 두 명령을 제시했다.

```bash
docker --version
docker info
```

명령의 의미는 다음과 같이 설명했다.

- `docker --version`: Docker CLI 버전 확인
- `docker info`: Docker 엔진 상태와 컨테이너 수 등의 정보 확인

또한 Docker 명령이 존재하는 것과 Docker 엔진이 동작하는 것은 다르므로 두 명령을 모두 확인해야 한다고 설명했다.

구조와 설명은 명확하지만 실제 출력 결과나 스크린샷이 없어 해당 환경에서 명령이 성공했는지는 문서만으로 확인하기 어렵다.

## 2. 적용할 방식

두 저장소의 장점을 합쳐 다음과 같이 기록한다.

- `docker --version`으로 Docker CLI 설치와 버전을 확인한다.
- `docker info`로 Docker 엔진 연결 상태를 확인한다.
- 전체 출력을 그대로 붙이지 않고 판별에 필요한 부분만 기록한다.
- 동일한 내용을 별도 체크리스트에 반복하지 않는다.
- 실제로 실행한 결과를 확인한 뒤 체크리스트를 완료 처리한다.
- Docker가 정상 동작한다면 설치 방법을 길게 설명하지 않는다.

README에 남길 핵심 정보는 다음과 같다.

- Docker 버전과 빌드 번호
- 현재 Docker Context
- Client와 Server 연결 여부
- 컨테이너와 이미지 개수
- Docker 엔진의 운영체제와 아키텍처

## 3. 수행할 명령

학교 맥에서 다음 명령을 실행한다.

```bash
docker --version
docker info
```

출력이 길더라도 원본은 그대로 확인한 뒤 README에는 필요한 부분만 추린다.

## 4. README 기록 형태

실제 출력 확인 후 아래 형식으로 작성한다.

````markdown
### 4-2) Docker 설치 및 점검

```console
$ docker --version
[실제 버전 출력]

$ docker info
Client:
 [버전과 Context]

Server:
 [컨테이너·이미지 개수]
 [운영체제와 아키텍처]
```
````

## 5. 완료 기준

다음 조건을 모두 확인한 후 Docker 설치/점검 체크리스트를 완료 처리한다.

- `docker --version`이 정상적으로 출력된다.
- `docker info`에 Client와 Server 정보가 모두 출력된다.
- Docker Context가 학교 환경의 OrbStack으로 확인된다.
- Docker CLI가 Docker 엔진과 정상적으로 통신한다.

## 6. 실제 출력 이해하기

### `docker --version`

```console
Docker version 28.5.2, build ecc6942
```

- `28.5.2`: 현재 터미널에서 사용하는 Docker CLI 버전이다.
- `ecc6942`: 해당 버전을 만든 소스 코드의 빌드 식별자다.
- 이 명령만 성공하면 Docker 명령 프로그램이 설치됐다는 것은 알 수 있지만 Docker 엔진이 실행 중인지는 알 수 없다.

Docker는 CLI가 명령을 보내고 Docker Engine이 실제 작업을 수행하는 Client/Server 구조다. 따라서 엔진 연결까지 확인하려면 `docker info` 또는 `docker version`의 Server 항목을 확인해야 한다.

### Client

```text
Client:
 Version:    28.5.2
 Context:    orbstack
 Debug Mode: false
```

- `Version`: Docker CLI 버전이다.
- `Context: orbstack`: 현재 CLI가 OrbStack에서 제공하는 Docker Engine을 대상으로 명령을 보내고 있다는 뜻이다.
- `Debug Mode: false`: Docker CLI의 상세 디버그 출력이 비활성화된 상태다.

### Client Plugins

```text
buildx: Docker Buildx
compose: Docker Compose
```

- `buildx`: Docker 이미지를 빌드할 때 사용하는 확장 기능이다. 이후 `docker build` 과정에서 사용된다.
- `compose`: 여러 컨테이너의 실행 설정을 YAML 파일로 관리하는 기능이다. 필수 과제 이후 보너스에서 사용할 수 있다.
- 플러그인의 `Path`는 사용자 홈 디렉토리 아래에 설치된 실행 파일 위치다.

### Server

```text
Server:
 Containers: 0
 Images: 0
 Server Version: 28.5.2
```

- `Server` 항목이 정상적으로 출력됐다는 사실 자체가 CLI와 Docker Engine의 통신 성공을 의미한다.
- `Containers: 0`: 아직 생성된 컨테이너가 없다.
- `Running`, `Paused`, `Stopped`: 컨테이너의 상태별 개수다.
- `Images: 0`: 아직 내려받거나 빌드한 이미지가 없다.
- `Server Version`: 실제 컨테이너를 관리하는 Docker Engine 버전이다.

현재는 깨끗한 초기 상태다. 이후 `hello-world`를 실행하면 이미지와 종료된 컨테이너 개수가 증가한다.

### Storage Driver

```text
Storage Driver: overlay2
Backing Filesystem: btrfs
```

- `overlay2`: 이미지의 여러 읽기 전용 레이어와 컨테이너의 쓰기 레이어를 겹쳐 하나의 파일 시스템처럼 보여주는 저장 방식이다.
- `btrfs`: OrbStack 내부 Linux 환경에서 `overlay2`가 사용하는 기반 파일 시스템이다.
- 이번 과제에서 직접 설정할 항목은 아니며, 이미지와 컨테이너 파일이 어떤 방식으로 관리되는지 보여주는 정보다.

### Logging Driver

```text
Logging Driver: json-file
```

컨테이너의 표준 출력과 표준 오류 로그를 JSON 형식으로 저장한다. 이후 `docker logs <container>`로 이 로그를 확인할 수 있다.

### Cgroup

```text
Cgroup Driver: cgroupfs
Cgroup Version: 2
```

Linux가 컨테이너별 CPU와 메모리 같은 자원 사용을 관리하는 방식이다. 이후 `docker stats`에서 컨테이너의 자원 사용량을 확인할 수 있다.

### Network와 Volume Plugins

```text
Volume: local
Network: bridge host ipvlan macvlan null overlay
```

- `local` 볼륨 드라이버를 사용해 Docker 볼륨을 만들 수 있다.
- `bridge`는 일반적인 단일 호스트 컨테이너 네트워크다.
- 이번 과제의 포트 매핑, 바인드 마운트, Docker 볼륨 실습에 필요한 기능이 제공되고 있다.

### Runtime

```text
Runtimes: io.containerd.runc.v2 runc
Default Runtime: runc
```

Docker Engine이 컨테이너 프로세스를 실제로 생성하고 실행할 때 사용하는 저수준 런타임이다. 기본 런타임은 `runc`다.

### Security Options

```text
Security Options:
 seccomp
  Profile: builtin
 cgroupns
```

- `seccomp`: 컨테이너에서 사용할 수 있는 Linux 시스템 호출을 제한한다.
- `cgroupns`: 컨테이너가 격리된 cgroup 정보를 보도록 한다.

### OrbStack 실행 환경

```text
Kernel Version: 6.17.8-orbstack-00308-g8f9c941121b1
Operating System: OrbStack
OSType: linux
Architecture: x86_64
CPUs: 6
Total Memory: 15.67GiB
Name: orbstack
```

- macOS에서 명령을 실행하고 있지만 컨테이너는 OrbStack이 제공하는 Linux 환경에서 실행된다.
- `x86_64`: 학교 맥과 OrbStack Docker Engine의 CPU 아키텍처다.
- `CPUs`, `Total Memory`: Docker Engine이 사용할 수 있는 자원이다.
- 이 값은 macOS 전체 자원과 정확히 같지 않을 수 있다.

### Docker Root Dir

```text
Docker Root Dir: /var/lib/docker
```

이미지, 컨테이너 레이어, 메타데이터 등 Docker Engine의 내부 데이터가 저장되는 Linux 환경의 경로다. macOS 호스트에서 직접 관리할 프로젝트 경로가 아니다.

### Swarm, Experimental, Live Restore

```text
Swarm: inactive
Experimental: false
Live Restore Enabled: false
```

- `Swarm: inactive`: Docker의 클러스터 기능을 사용하지 않고 있다.
- `Experimental: false`: 실험 기능이 비활성화됐다.
- `Live Restore Enabled: false`: Docker 데몬이 재시작될 때 컨테이너를 계속 실행시키는 기능이 비활성화됐다.
- 모두 이번 필수 과제에서는 변경할 필요가 없다.

### Insecure Registries와 Address Pools

- `Insecure Registries`의 `127.0.0.0/8`, `::1/128`은 로컬 루프백 주소 범위다.
- `Default Address Pools`는 Docker가 컨테이너 네트워크를 만들 때 할당할 내부 IP 주소 범위다.
- 이번 과제에서 직접 수정할 필요는 없다.

### 마지막 경고

```text
WARNING: DOCKER_INSECURE_NO_IPTABLES_RAW is set
```

Docker Engine이 Linux `iptables`의 `raw` 테이블 규칙을 만들지 않는 설정으로 실행되고 있다는 경고다. Docker Engine 28 릴리스 노트에 따르면 이 설정은 일부 네트워크 보안 강화를 우회하므로 운영 환경에는 권장되지 않는다.

이번 학교 맥의 로컬 실습에서는 다음 이유로 Docker 설치·점검 실패로 판단하지 않는다.

- `docker info`의 Server 항목이 정상적으로 출력됐다.
- OrbStack Engine과 통신하고 있다.
- 이미지와 컨테이너 실행에 필요한 기능이 확인됐다.

다만 이 경고를 보고 “아무 의미가 없다”고 판단해서는 안 된다. 외부에 서비스를 배포하는 운영 환경이라면 네트워크 노출 범위를 별도로 검토해야 한다. 학교 맥의 OrbStack 설정은 임의로 변경하지 않고 그대로 사용한다.

참고:

- [Docker system info](https://docs.docker.com/reference/cli/docker/system/info/)
- [Docker version](https://docs.docker.com/reference/cli/docker/version/)
- [Docker Engine 28 release notes](https://docs.docker.com/engine/release-notes/28/)

## 7. 이번 출력으로 확인된 결과

- Docker CLI 28.5.2가 설치돼 있다.
- 현재 Context는 OrbStack이다.
- Docker Engine 28.5.2가 실행 중이다.
- Client와 Server가 정상적으로 통신한다.
- 아직 이미지와 컨테이너가 없는 초기 상태다.
- 다음 단계로 `hello-world` 이미지를 내려받아 컨테이너 실행을 확인할 수 있다.

## 8. 권한 변경 실습 진행 시점

권한 변경 실습은 지금 별도의 연습 파일로 진행하지 않는다. Nginx 컨테이너에서 `site/index.html`을 읽지 못하는 상황을 만든 뒤 다음 순서로 진행한다.

1. `ls -l`과 `ls -ld`로 파일과 디렉토리 권한을 확인한다.
2. Nginx가 파일을 읽거나 디렉토리에 접근하지 못하는 현상을 확인한다.
3. `chmod`로 필요한 권한을 변경한다.
4. 변경 전·후 권한을 비교한다.
5. Nginx에서 페이지가 다시 표시되는지 확인한다.

이 방식은 권한 숫자만 바꾸는 별도 실습보다 `r`, `w`, `x`가 실제 서비스에 어떤 영향을 주는지 함께 확인할 수 있다.
