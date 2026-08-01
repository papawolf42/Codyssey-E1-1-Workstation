# COPY 기반 권한 변경 실습

## 1. instruction 근거

`instruction.md`에서 권한 실습을 요구하는 핵심 부분은 다음과 같다.

- 117행: `권한 실습 및 증거 기록`
- 118행: 권한 확인·변경 명령을 수행하고 변경 전·후 비교를 기술 문서에 기록
- 119행: 파일 1개와 디렉터리 1개에 대한 권한 변경 실험
- 225행: 결과 예시의 `권한 변경 실습` 체크 항목

instruction에는 `chmod`라는 명령어가 직접 적혀 있지 않다. 대신 권한을 확인하고 변경하라고 요구하므로 이 실습에서는 `ls -l`, `ls -ld`, `chmod`를 사용한다.

## 2. 실습 목적

명령어 사용 연습에 그치지 않고, 워크스페이스의 `site/index.html` 권한이 Dockerfile의 `COPY`를 통해 이미지 내부 파일에 어떻게 반영되는지 확인한다.

현재 Dockerfile은 다음 파일을 Nginx 웹 문서 경로에 복사한다.

```dockerfile
COPY site/index.html /usr/share/nginx/html/index.html
```

로컬 디렉터리를 빌드 컨텍스트로 사용할 때 `COPY`는 일반적으로 파일의 권한 비트를 보존한다. 다만 `--chown`을 지정하지 않았으므로 이미지 내부 파일의 소유자는 기본적으로 `root:root`가 된다.

권한을 제한한 이미지와 복구한 이미지를 각각 빌드하여 다음 내용을 관찰한다.

- 호스트 파일 권한
- 이미지 내부 파일 권한
- 권한에 따른 Nginx 응답
- 파일과 디렉터리의 변경 전·후 권한

## 3. 기록 방식

이 실습은 별도의 제출 스크린샷을 추가하지 않고 README에 텍스트 로그로 기록한다.

- 명령어와 핵심 출력은 코드 블록으로 남긴다.
- 긴 빌드 출력은 `FINISHED`, `COPY`, 이미지 이름 등 핵심 부분만 사용한다.
- 예상과 다른 결과가 나오더라도 실제 결과를 그대로 기록한다.
- 계획한 다섯 번째 스크린샷은 GitHub·VS Code 연동 증거로 남겨둔다.

## 4. 수행 시나리오

### 4-1. 현재 권한 확인

```bash
cd ~/Dev/Codyssey-E1-1-Workstation/mandatory

ls -ld site
ls -l site/index.html
```

### 4-2. 파일 권한을 600으로 변경

```bash
chmod 600 site/index.html
ls -l site/index.html
```

`600`은 소유자에게만 읽기와 쓰기 권한을 주고 그룹과 기타 사용자에게는 아무 권한도 주지 않는다.

### 4-3. 권한 테스트 이미지 빌드

기존 `first-built-image`와 구분하기 위해 별도의 이미지 이름을 사용한다.

```bash
docker build --no-cache -t permission-test-image .
```

이미지 내부에 복사된 파일 권한을 확인한다.

```bash
docker run --rm permission-test-image \
  ls -l /usr/share/nginx/html/index.html
```

호스트의 `600` 권한이 이미지 내부 파일에도 반영됐는지 비교한다.

### 4-4. 제한된 권한에서 Nginx 동작 확인

기존 컨테이너와 포트가 겹치지 않도록 8082번 포트를 사용한다.

```bash
docker run -d \
  --name permission-test-container \
  -p 8082:80 \
  permission-test-image

curl -i http://localhost:8082/
docker logs permission-test-container
```

가능한 결과는 다음과 같다.

- `403 Forbidden`: Nginx 작업 프로세스가 파일을 읽지 못함
- `200 OK`: 현재 Nginx 실행 구조에서 해당 파일을 읽을 수 있었음

어느 결과가 나오더라도 실험 실패로 판단하지 않고 실제 관찰 결과를 기록한다.

### 4-5. 테스트 컨테이너 정리

```bash
docker stop permission-test-container
docker rm permission-test-container
```

### 4-6. 파일 권한을 644로 복구

```bash
chmod 644 site/index.html
ls -l site/index.html

docker build --no-cache -t permission-test-image .
docker run --rm permission-test-image \
  ls -l /usr/share/nginx/html/index.html
```

`644`는 소유자에게 읽기와 쓰기 권한을, 그룹과 기타 사용자에게 읽기 권한을 준다.

필요하면 복구된 이미지로 Nginx를 다시 실행하고 `200 OK`를 확인한다.

### 4-7. 디렉터리 권한 변경과 복구

```bash
ls -ld site

chmod 700 site
ls -ld site

chmod 755 site
ls -ld site
```

- `700`: 소유자만 읽기·쓰기·진입 가능
- `755`: 소유자는 읽기·쓰기·진입, 그룹과 기타 사용자는 읽기·진입 가능
- 디렉터리의 실행 권한(`x`): 디렉터리 안의 항목에 접근하기 위한 진입 권한

실습 후에는 `site`를 `755`, `site/index.html`을 `644`로 복구한다.

## 5. README에 남길 내용

실제 수행 후 README에는 다음 내용만 간결하게 정리한다.

- 파일 권한 `644 → 600 → 644`
- 이미지 내부에 복사된 파일 권한
- 제한된 권한에서 관찰한 Nginx 응답
- 디렉터리 권한 `755 → 700 → 755`
- `r/w/x`, `600`, `644`, `700`, `755`의 의미
- 실습 종료 후 원래 권한으로 복구했다는 사실

명령 실행과 출력 확인이 끝난 항목만 체크리스트에서 `[x]`로 표시한다.
