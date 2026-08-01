# 바인드 마운트 과제 요구사항 분석

## 1. instruction에서 직접 요구하는 내용

바인드 마운트와 관련된 핵심 요구는 `instruction.md` 79~81행이다.

```text
79  7. 바인드 마운트 반영 + 볼륨 영속성 증거
80     - 바인드 마운트: 실행 명령 + 호스트 변경 전/후 비교
81     - Docker 볼륨: 생성/연결/검증 명령 + 컨테이너 삭제 전/후 비교
```

바인드 마운트에 대해 직접 요구하는 것은 다음 두 가지다.

1. 바인드 마운트로 컨테이너를 실행한 명령
2. 호스트 파일을 변경하기 전과 변경한 후의 결과 비교

즉, 마운트 옵션을 사용했다는 사실만 기록해서는 부족하다. 호스트 파일을 수정했을 때 이미지를 다시 빌드하거나 컨테이너를 다시 생성하지 않아도 변경된 내용이 컨테이너 응답에 반영되는지 확인해야 한다.

## 2. 관련 공통 요구

### README 체크리스트와 검증 방법

`instruction.md` 102~110행은 README에 수행 항목과 검증 방법을 기록하도록 요구한다.

```text
102  제출 저장소 및 기술 문서
104  기술 문서가 반드시 포함해야 할 내용
108  수행 항목 체크리스트에 마운트 포함
109  어떤 명령으로 무엇을 확인했는지와 결과 위치 또는 증거 링크
110  명령과 출력을 코드 블록으로 정리
```

바인드 마운트 실습이 끝나면 README 체크리스트를 `[x]`로 변경하고, 실행 명령과 변경 전·후 출력을 코드 블록으로 남겨야 한다.

### CLI에서 직접 설정하고 검증

`instruction.md` 196~199행은 포트 매핑과 마운트·볼륨을 터미널에서 직접 설정하고 동작을 확인하도록 요구한다.

```text
196  실행 방식
197  모든 작업은 터미널 기반으로 수행
199  포트 매핑과 마운트/볼륨은 직접 설정하고 동작을 검증
```

Docker Desktop 화면에서 마운트를 설정하는 방식보다 `docker run -v ...` 또는 `docker run --mount ...` 명령을 사용하는 것이 요구사항에 맞다.

### 명령과 출력이 함께 있어야 함

`instruction.md` 201~202행은 증거에 명령어 입력과 출력 결과가 함께 포함되어야 한다고 명시한다.

```text
201  증거 수집 규칙
202  캡처/로그에는 명령어 입력과 출력 결과가 함께 포함
```

README에는 명령만 나열하지 않고 `cat`과 `curl`에서 확인한 실제 결과도 함께 기록해야 한다.

### 재현 가능한 경로 사용

`instruction.md` 206~208행은 README만 보고 같은 결과를 재현할 수 있어야 하며, 특정 PC에 종속된 경로가 있으면 대안을 적도록 요구한다.

```text
206  재현성
207  README만 보고 평가자가 동일 절차를 따라 결과를 확인
208  특정 개인 PC에 종속된 경로·설정에는 대체 방법 또는 주의사항 기록
```

학교 Mac이나 집 Mac의 절대 경로를 직접 쓰는 대신 `mandatory` 디렉터리로 이동한 뒤 `$(pwd)`를 사용하면 두 환경에서 같은 명령을 사용할 수 있다.

## 3. 결과 예시의 위치

`instruction.md` 223~232행의 결과 예시에는 다음 체크 항목이 있다.

```text
230  - [x] 바인드 마운트 반영
```

이 부분은 제출 형식의 참고 예시이며, 실습 방법이나 명령을 지정하는 요구사항은 아니다. 실제 수행 결과가 확인된 뒤 README의 현재 세부 체크리스트를 완료 처리하면 된다.

## 4. instruction이 요구하지 않는 것

다음 사항은 바인드 마운트의 필수 요구가 아니다.

- 특정 호스트 절대 경로 사용
- 특정 포트 번호 사용
- `-v`와 `--mount` 중 특정 문법 사용
- 바인드 마운트 전용 스크린샷
- 바인드 마운트 때문에 이미지 다시 빌드
- 컨테이너를 두 번 이상 재생성
- 이미지 ID나 컨테이너 ID 일치
- 변경된 HTML을 최종 저장소에 그대로 남김

명령과 출력 로그로 변경 전·후를 증명하면 스크린샷을 추가하지 않아도 된다.

## 5. 현재 프로젝트에 맞는 수행 방법

현재 `first-container`가 호스트 8080번 포트를 사용하고 있으므로 바인드 마운트용 컨테이너는 8081번 포트를 사용한다.

마운트 대상은 현재 프로젝트의 `mandatory/site/index.html`이다. 컨테이너에서는 Nginx 기본 문서 경로인 `/usr/share/nginx/html/index.html`에 연결한다.

```text
호스트:
mandatory/site/index.html

컨테이너:
/usr/share/nginx/html/index.html

포트:
8081:80
```

읽기 전용 옵션 `:ro`를 사용해 컨테이너가 호스트 파일을 수정하지 못하게 한다. 호스트에서 파일을 변경하는 것은 가능하며 변경된 내용은 컨테이너에 바로 반영된다.

## 6. 권장 실행 순서

### 6-1. 프로젝트 경로와 변경 전 내용 확인

```bash
cd mandatory
pwd
cat site/index.html
```

예상 내용:

```html
<h1>I'm html file</h1>
```

### 6-2. 바인드 마운트 컨테이너 실행

```bash
docker run -d \
  --name bind-container \
  -p 8081:80 \
  -v "$(pwd)/site/index.html:/usr/share/nginx/html/index.html:ro" \
  first-built-image
```

상태와 마운트 정보를 확인한다.

```bash
docker ps
docker inspect bind-container \
  --format '{{range .Mounts}}{{.Type}}: {{.Source}} -> {{.Destination}} (RW={{.RW}}){{end}}'
```

예상 핵심 정보:

```text
bind: .../site/index.html -> /usr/share/nginx/html/index.html (RW=false)
```

### 6-3. 변경 전 응답 확인

```bash
curl http://localhost:8081/
```

예상 응답:

```html
<h1>I'm html file</h1>
```

### 6-4. 호스트 파일 변경

```bash
echo "<h1>Bind mount html file</h1>" > site/index.html
cat site/index.html
```

변경 후 호스트 내용:

```html
<h1>Bind mount html file</h1>
```

### 6-5. 변경 반영 확인

이미지를 다시 빌드하거나 컨테이너를 다시 시작하지 않고 같은 주소로 요청한다.

```bash
curl http://localhost:8081/
```

예상 응답:

```html
<h1>Bind mount html file</h1>
```

이 결과가 나오면 호스트 파일 변경이 실행 중인 컨테이너에 즉시 반영된 것이다.

### 6-6. 호스트 파일 복구

```bash
echo "<h1>I'm html file</h1>" > site/index.html
cat site/index.html
curl http://localhost:8081/
```

최종 응답:

```html
<h1>I'm html file</h1>
```

### 6-7. 테스트 컨테이너 정리

```bash
docker rm -f bind-container
```

`first-container`와 `first-built-image`는 삭제하지 않는다.

## 7. README에 남겨야 할 최소 증거

README에는 다음 흐름을 확인할 수 있는 실제 명령과 출력을 남긴다.

```text
cat 변경 전
→ docker run -v
→ curl 변경 전
→ 호스트 파일 변경
→ cat 변경 후
→ curl 변경 후
→ 원래 내용 복구
```

핵심 비교:

```text
호스트 파일:
<h1>I'm html file</h1>
→ <h1>Bind mount html file</h1>
→ <h1>I'm html file</h1>

컨테이너 응답:
<h1>I'm html file</h1>
→ <h1>Bind mount html file</h1>
→ <h1>I'm html file</h1>
```

이 비교만 명확하면 바인드 마운트의 필수 요구를 충족한다.

## 8. 수행 시 주의사항

- 명령은 저장소 루트가 아니라 `mandatory` 디렉터리에서 실행한다.
- `$(pwd)` 전체를 큰따옴표로 감싸 경로에 공백이 있어도 동작하도록 한다.
- `bind-container`가 이미 있으면 새 컨테이너를 만들기 전에 기존 상태를 확인한다.
- 실습 후 `site/index.html`을 원래 내용으로 복구한다.
- 최종 `git diff -- site/index.html`에서 변경이 남지 않았는지 확인한다.
- 컨테이너 ID와 이미지 해시는 환경마다 달라도 문제가 없다.
- 로그와 스크린샷에 토큰·비밀번호·인증 코드가 포함되지 않았는지 확인한다.

## 9. 분석 결론

이 과제에서 바인드 마운트의 핵심은 호스트 파일과 컨테이너 파일이 실행 중에 연결돼 있다는 사실을 직접 확인하는 것이다.

현재 프로젝트에서는 `site/index.html`을 Nginx 문서 경로에 읽기 전용으로 연결하고, 호스트 파일을 변경한 뒤 `curl` 응답이 즉시 달라지는 것을 기록하면 된다. 절대 경로, 이미지 해시, 컨테이너 ID를 환경 간에 일치시킬 필요는 없다.
