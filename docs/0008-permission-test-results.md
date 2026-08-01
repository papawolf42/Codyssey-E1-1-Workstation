# Docker 권한 실험 결과

## 1. 실험 목적

학교 Mac에서 권한 실습을 수행하기 전에 현재 Mac에서 여러 권한을 시험하여, 실제로 의미 있는 비교와 필요한 명령만 추린다.

이번 실험에서는 저장소 원본을 변경하지 않고 임시 빌드 컨텍스트와 고유한 Docker 이미지·컨테이너를 사용했다. 실험 종료 후 생성한 자원은 모두 정리했다.

## 2. 실행 환경

현재 Mac의 Docker 환경은 학교 Mac의 OrbStack과 다르다.

```text
Docker context: desktop-linux
Docker daemon: Docker Desktop 28.5.2
Kernel: linuxkit 6.12.54
```

따라서 이미지에 파일을 저장하는 `COPY` 결과는 학교 Mac에서도 비슷할 가능성이 높지만, 호스트 파일을 실시간 공유하는 바인드 마운트 결과는 OrbStack에서 달라질 수 있다.

## 3. COPY와 파일 권한

현재 프로젝트와 같은 방식으로 `site/index.html`을 Nginx 웹 문서 경로에 복사했다.

```dockerfile
COPY site/index.html /usr/share/nginx/html/index.html
```

각 권한으로 이미지를 새로 빌드한 뒤 이미지 내부 권한, 소유자, Nginx 응답을 확인했다.

| 호스트 파일 권한 | 이미지 내부 권한 | 이미지 내부 소유자 | Nginx 응답 |
|---:|---:|---|---:|
| `000` | 빌드 실패 | 없음 | 없음 |
| `400` | `400` | `root:root` | `403` |
| `600` | `600` | `root:root` | `403` |
| `640` | `640` | `root:root` | `403` |
| `644` | `644` | `root:root` | `200` |
| `755` | `755` | `root:root` | `200` |

### 핵심 결과

- `COPY`는 호스트 파일의 권한 비트를 이미지 내부 파일에 보존했다.
- `COPY --chown`을 사용하지 않았으므로 이미지 내부 소유자는 `root:root`가 됐다.
- Nginx 작업 프로세스는 일반 사용자이므로 `400`, `600`, `640`의 `root:root` 파일을 읽지 못했다.
- 다른 사용자에게 읽기 권한이 있는 `644`와 `755`에서는 `200 OK`가 반환됐다.
- HTML 파일에는 실행 권한이 필요하지 않으므로 정상 운영 권한으로는 `755`보다 `644`가 적절하다.

권한이 부족한 경우 Nginx 로그에서 다음 오류를 확인했다.

```text
open() "/usr/share/nginx/html/index.html" failed (13: Permission denied)
```

### `000`에서 빌드가 실패한 이유

`000`은 소유자에게도 읽기 권한이 없다. Docker가 빌드 컨텍스트의 파일을 읽어 이미지에 전달하는 단계에서 다음과 같은 권한 오류가 발생했다.

```text
permission denied
```

따라서 과제 기록에는 빌드 자체가 실패하는 `000`보다, 빌드는 성공하지만 Nginx 접근이 실패하는 `600`과 정상 응답을 반환하는 `644`를 비교하는 편이 흐름이 명확하다.

## 4. COPY와 디렉터리 권한

디렉터리를 이미지 내부에 함께 복사하는 별도 실험에서 다음 결과를 확인했다.

| 디렉터리 권한 | 이미지 내부 권한 | Nginx 응답 |
|---:|---:|---:|
| `700` | `700` | `403` |
| `711` | `711` | `200` |
| `750` | `750` | `403` |
| `755` | `755` | `200` |

Nginx 사용자가 디렉터리 안의 파일에 접근하려면 경로에 포함된 디렉터리에 실행 권한(`x`)이 필요하다.

- `700`: 소유자만 진입할 수 있으므로 Nginx 사용자가 접근하지 못함
- `711`: 다른 사용자에게도 실행 권한이 있어 파일 경로에 접근 가능
- `750`: 그룹이 `root`이므로 Nginx 사용자가 접근하지 못함
- `755`: 모든 사용자가 읽고 진입할 수 있어 정상 접근

### 현재 Dockerfile과의 차이

현재 Dockerfile은 디렉터리 전체가 아니라 파일 하나만 복사한다.

```dockerfile
COPY site/index.html /usr/share/nginx/html/index.html
```

이 경우 호스트의 `site` 디렉터리 권한은 이미지에 전달되지 않는다. `index.html`의 권한만 보존되고, 목적지인 `/usr/share/nginx/html` 디렉터리는 베이스 이미지의 기존 권한을 사용한다.

디렉터리 권한 보존을 시험하려면 디렉터리가 이미지 내부의 새 경로에 포함되도록 별도의 Dockerfile 구성이 필요하다.

## 5. 바인드 마운트와의 차이

Docker Desktop의 바인드 마운트에서는 COPY와 다른 결과가 나타났다.

| 호스트 조건 | 비-root 읽기 | Nginx 응답 |
|---|---:|---:|
| 파일 `000`, 디렉터리 `755` | 실패 | `403` |
| 파일 `600`, 디렉터리 `755` | 성공 | `200` |
| 파일 `644`, 디렉터리 `755` | 성공 | `200` |
| 파일 `644`, 디렉터리 `700` | 성공 | `200` |
| 파일 `644`, 디렉터리 `755` | 성공 | `200` |

바인드 마운트는 Docker Desktop이 macOS 파일을 Linux 컨테이너에 실시간으로 공유하는 과정에서 소유권과 접근을 중계한다. 이 때문에 `600` 파일이나 `700` 디렉터리도 컨테이너에서 접근할 수 있었다.

정리하면 다음과 같다.

- `COPY`: 빌드 시 파일을 이미지 레이어에 새로 저장하고 기본 소유자는 `root:root`가 됨
- 바인드 마운트: 호스트 파일을 컨테이너에 실시간으로 공유하며 런타임의 파일 공유 방식에 영향을 받음

학교 Mac은 OrbStack을 사용하므로 바인드 마운트 권한 결과가 현재 Mac의 Docker Desktop과 같다고 단정하지 않는다. 학교 Mac에서 나온 실제 결과를 그대로 기록한다.

## 6. 학교 Mac 권장 실습

파일 권한은 `600 → 403`, `644 → 200` 비교를 우선 수행한다.

### 6-1. 600 권한 확인

```bash
cd ~/Dev/Codyssey-E1-1-Workstation/mandatory

chmod 600 site/index.html
ls -l site/index.html

docker build --no-cache -t permission-test-image .

docker run --rm permission-test-image \
  ls -l /usr/share/nginx/html/index.html

docker run -d \
  --name permission-test-container \
  -p 8082:80 \
  permission-test-image

curl -i http://localhost:8082/
docker logs --tail 2 permission-test-container
```

예상 결과:

```text
이미지 내부 권한: 600 root:root
HTTP 응답: 403 Forbidden
Nginx 로그: Permission denied
```

### 6-2. 테스트 컨테이너 정리

```bash
docker rm -f permission-test-container
```

### 6-3. 644 권한 복구 및 확인

```bash
chmod 644 site/index.html
ls -l site/index.html

docker build --no-cache -t permission-test-image .

docker run --rm permission-test-image \
  ls -l /usr/share/nginx/html/index.html

docker run -d \
  --name permission-test-container \
  -p 8082:80 \
  permission-test-image

curl -i http://localhost:8082/
```

예상 결과:

```text
이미지 내부 권한: 644 root:root
HTTP 응답: 200 OK
```

### 6-4. 최종 정리

```bash
docker rm -f permission-test-container
docker image rm permission-test-image

chmod 755 site
chmod 644 site/index.html

ls -ld site
ls -l site/index.html
```

## 7. README 기록 범위

실제 수행 후 README에는 다음 내용만 남긴다.

- 호스트 파일 권한 `600 → 644`
- 이미지 내부 파일 권한과 `root:root` 소유자
- `600`에서 관찰한 Nginx 응답과 로그
- `644` 복구 후 확인한 `200 OK`
- 파일 권한에서 `r/w/x`, `600`, `644`의 의미
- 디렉터리 권한 변경 전·후와 `700`, `755`, 실행 권한(`x`)의 의미
- 실습 종료 후 `site=755`, `site/index.html=644`로 복구했다는 사실

학교 Mac의 결과가 예상과 다르면 실패로 꾸미지 않고 실제 결과와 실행 환경의 차이를 기록한다.
