# 권한 변경과 바인드 마운트 실습 계획

## 1. 왜 권한을 변경하는가

`chmod` 명령 자체를 연습하는 데서 끝내지 않고, 이 프로젝트의 Nginx 웹 서버가 `site/index.html`에 접근할 때 파일과 디렉터리 권한이 어떤 역할을 하는지 확인한다.

- 파일의 읽기 권한(`r`): Nginx가 `index.html`의 내용을 읽는 데 필요하다.
- 디렉터리의 실행 권한(`x`): Nginx가 디렉터리 안으로 들어가 파일에 접근하는 데 필요하다.
- 권한이 부족하면 웹 페이지를 제공하지 못하거나 `403 Forbidden` 등의 오류가 발생할 수 있다.
- 권한을 복구한 뒤 다시 정상 응답을 확인하면 변경 전·후의 차이를 비교할 수 있다.

## 2. 바인드 마운트와 함께 진행하는 이유

Dockerfile의 `COPY`로 이미지 안에 들어간 파일은 이미지를 빌드할 때 복사된 결과다. 이후 호스트의 `site/index.html` 권한을 변경해도 기존 이미지 안의 파일에는 바로 반영되지 않는다.

반면 바인드 마운트는 호스트 파일을 컨테이너 경로에 직접 연결한다.

```bash
docker run -d \
  --name bind-nginx-container \
  -p 8081:80 \
  -v "$(pwd)/site/index.html:/usr/share/nginx/html/index.html:ro" \
  first-built-image
```

따라서 호스트 파일의 내용이나 접근 조건을 바꾼 뒤 컨테이너의 반응을 관찰할 수 있다. 같은 실습 안에서 다음 두 요구사항을 자연스럽게 연결할 수 있다.

- 호스트 파일 변경이 컨테이너에 반영되는지 확인하는 바인드 마운트 실습
- 파일과 디렉터리의 권한 변경 전·후를 비교하는 권한 실습

## 3. 권장 수행 순서

### 3-1. 현재 권한과 정상 접속 확인

```bash
cd ~/Dev/Codyssey-E1-1-Workstation/mandatory

ls -l site/index.html
ls -ld site

docker run -d \
  --name bind-nginx-container \
  -p 8081:80 \
  -v "$(pwd)/site/index.html:/usr/share/nginx/html/index.html:ro" \
  first-built-image

curl -i http://localhost:8081/
```

정상 권한에서 `200 OK`와 현재 HTML 내용이 출력되는지 확인한다.

### 3-2. 호스트 파일 변경 반영 확인

`site/index.html`의 내용을 변경하고 다시 접속한다.

```bash
echo "<h1>Bind mount html file</h1>" > site/index.html
cat site/index.html
curl -i http://localhost:8081/
```

이미지를 다시 빌드하거나 컨테이너를 다시 만들지 않았는데도 변경된 내용이 출력되면 바인드 마운트가 반영된 것이다.

### 3-3. 파일 권한 변경

```bash
ls -l site/index.html
chmod 000 site/index.html
ls -l site/index.html
curl -i http://localhost:8081/

chmod 644 site/index.html
ls -l site/index.html
curl -i http://localhost:8081/
```

`000`은 누구에게도 읽기·쓰기·실행 권한을 주지 않는다. 실험 후에는 소유자가 읽고 쓸 수 있고 나머지는 읽을 수 있는 `644`로 복구한다.

### 3-4. 디렉터리 권한 변경

```bash
ls -ld site
chmod 700 site
ls -ld site
chmod 755 site
ls -ld site
```

`700`은 소유자만 디렉터리에 접근할 수 있게 하고, `755`는 소유자에게 읽기·쓰기·실행 권한을, 나머지 사용자에게 읽기·실행 권한을 준다. 실험 후에는 `755`로 복구한다.

### 3-5. 실습 종료

```bash
docker stop bind-nginx-container
docker rm bind-nginx-container
```

## 4. macOS와 OrbStack에서 주의할 점

macOS의 파일을 Linux 컨테이너에 공유할 때 OrbStack이 중간에서 파일 시스템 접근을 처리한다. 이 때문에 호스트에서 `chmod`로 권한을 제한해도 컨테이너에서 예상한 것과 똑같이 `403 Forbidden`이 발생하지 않을 수 있다.

실제 결과에 따라 다음처럼 기록한다.

- 접속이 실패한 경우: 권한 제한으로 Nginx가 파일을 읽지 못한 결과와 복구 후 정상 응답을 비교한다.
- 접속이 계속 성공한 경우: 결과를 실패로 꾸미지 않고, OrbStack의 파일 공유 환경에서는 호스트 권한 변화가 컨테이너에 동일하게 적용되지 않았다고 기록한다.

권한 오류가 반드시 발생해야 실습이 성공하는 것은 아니다. 명령을 수행하고 변경 전·후 권한과 실제 동작을 관찰한 결과를 그대로 남기는 것이 중요하다.

## 5. README에 남길 범위

README에는 전체 시행착오를 모두 복사하지 않고 다음 내용만 남긴다.

- 파일과 디렉터리의 변경 전·후 권한
- `644`, `755`와 `r/w/x`의 의미
- 바인드 마운트 실행 명령
- 호스트 HTML 변경 전·후의 응답
- 권한 변경 뒤 실제로 관찰된 결과
- 실습 후 원래 권한으로 복구했다는 내용

실제 명령과 출력이 준비된 뒤 수행한 체크리스트만 `[x]`로 변경한다.
