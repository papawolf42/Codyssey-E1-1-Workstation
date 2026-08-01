# Nginx 디렉터리 644 권한 실험

## 1. 실험 목적

Nginx가 HTML 파일을 제공할 때 파일의 읽기 권한뿐 아니라 상위 디렉터리의 실행 권한(`x`)도 필요한지 확인한다.

파일 권한의 영향을 섞지 않기 위해 `index.html`은 실험 내내 `644`로 유지하고 `/usr/share/nginx/html` 디렉터리의 권한만 변경했다.

```text
변경한 대상: /usr/share/nginx/html
유지한 대상: /usr/share/nginx/html/index.html
```

## 2. 실행 환경

```text
Docker context: desktop-linux
Docker daemon: Docker Desktop 28.5.2
테스트 포트: 18081
```

저장소 원본을 수정하지 않고 별도의 테스트 이미지와 컨테이너를 사용했다. 실험 후 테스트 자원은 모두 삭제했다.

## 3. 최초 상태

디렉터리와 파일의 권한을 각각 확인했다.

```text
디렉터리: drwxr-xr-x 755 root:root
파일:      -rw-r--r-- 644 root:root
```

최초 HTTP 응답은 정상이었다.

```text
HTTP=200
```

## 4. 디렉터리만 644로 변경

다음 명령으로 `html` 디렉터리만 변경했다.

```bash
docker exec codex-dir644-test-container \
  chmod 644 /usr/share/nginx/html
```

`index.html`에는 `chmod`를 실행하지 않았다.

변경 후 상태:

```text
디렉터리: drw-r--r-- 644 root:root
파일:      -rw-r--r-- 644 root:root
```

두 대상 모두 숫자로는 `644`지만 파일과 디렉터리에서 각 권한의 역할은 다르다.

## 5. 관찰 결과

### 5-1. 디렉터리 목록

디렉터리에 읽기 권한(`r`)이 있으므로 내부 파일 이름은 확인할 수 있었다.

```text
50x.html
index.html
```

### 5-2. 파일 내용 접근

Nginx 사용자로 `index.html`을 읽으려고 하자 실패했다.

```text
cat: can't open '/usr/share/nginx/html/index.html': Permission denied
```

파일 자체에는 다른 사용자의 읽기 권한이 있었지만, 상위 디렉터리에 실행 권한(`x`)이 없어서 파일 경로를 통과하지 못했다.

### 5-3. HTTP 응답

```text
HTTP=403
```

Nginx 로그에서도 디렉터리 권한으로 인한 접근 실패를 확인했다.

```text
"/usr/share/nginx/html/index.html" is forbidden
(13: Permission denied)

"GET / HTTP/1.1" 403
```

## 6. 디렉터리를 755로 복구

```bash
docker exec codex-dir644-test-container \
  chmod 755 /usr/share/nginx/html
```

복구 결과:

```text
디렉터리: drwxr-xr-x 755 root:root
파일:      -rw-r--r-- 644 root:root
HTTP=200
```

## 7. 권한 해석

### 디렉터리 644

```text
644 = rw-r--r--
```

- `r`: 디렉터리에 들어 있는 파일 이름을 읽을 수 있음
- `w`: 소유자가 디렉터리 항목을 변경할 수 있음
- `x` 없음: 디렉터리를 통과하여 내부 파일에 접근할 수 없음

따라서 파일 이름은 보이지만 `index.html`의 내용은 읽을 수 없었다.

### 디렉터리 755

```text
755 = rwxr-xr-x
```

- 소유자: 읽기·쓰기·진입 가능
- 그룹과 기타 사용자: 읽기·진입 가능
- Nginx 사용자도 `x` 권한으로 디렉터리를 통과할 수 있음

따라서 `index.html`에 접근할 수 있고 `200 OK`가 반환됐다.

## 8. 결론

이번 실험에서는 파일을 계속 `644`로 유지하고 디렉터리만 변경했다.

```text
디렉터리: 755 → 644 → 755
파일:     644 → 644 → 644
HTTP:     200 → 403 → 200
```

결과적으로 Nginx가 HTML을 제공하려면 다음 두 조건이 모두 필요하다.

1. HTML 파일에 읽기 권한(`r`)이 있어야 한다.
2. 파일까지 이어지는 디렉터리에 실행 권한(`x`)이 있어야 한다.

파일의 읽기 권한과 디렉터리의 실행 권한 중 하나라도 없으면 Nginx는 파일에 접근하지 못하고 `403 Forbidden`을 반환한다.

## 9. 학교 Mac에서 재현할 명령

실행 중인 `first-container`를 사용한다.

```bash
docker exec first-container \
  ls -ld /usr/share/nginx/html

docker exec first-container \
  ls -l /usr/share/nginx/html/index.html

curl -i http://localhost:8080/

docker exec first-container \
  chmod 644 /usr/share/nginx/html

docker exec first-container \
  ls -ld /usr/share/nginx/html

docker exec first-container \
  ls -l /usr/share/nginx/html/index.html

curl -i http://localhost:8080/
docker logs --tail 2 first-container

docker exec first-container \
  chmod 755 /usr/share/nginx/html

curl -i http://localhost:8080/
```

마지막에는 반드시 다음 상태로 복구됐는지 확인한다.

```text
/usr/share/nginx/html             755
/usr/share/nginx/html/index.html  644
HTTP                              200 OK
```
