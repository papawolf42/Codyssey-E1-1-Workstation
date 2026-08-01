# Codyssey E1-1 필수 과제 5시간 진행 계획

## 진행 원칙

- 학교 맥에서 명령을 실행하고 전체 결과를 복사한다.
- 실제 출력 확인 후 `mandatory/README.md`에 핵심 결과를 기록한다.
- 한 단계가 끝날 때마다 체크리스트를 갱신한다.
- 스크린샷은 브라우저 접속과 GitHub/VS Code 연동처럼 화면 증거가 필요한 시점에 촬영한다.
- 권한 변경은 별도 연습 파일 대신 Nginx의 `index.html` 접근 문제와 연결한다.
- 커밋 전에는 변경 내용을 검토하고 승인한 뒤 커밋한다.

## 전체 일정

| 단계 | 작업 | 예상 시간 |
|---|---|---:|
| 1 | Docker 설치 및 점검 | 15분 |
| 2 | hello-world와 Docker 기본 운영 | 35분 |
| 3 | Dockerfile과 Nginx 이미지 | 40분 |
| 4 | Nginx 권한 문제 재현과 복구 | 35분 |
| 5 | 바인드 마운트 반영 | 30분 |
| 6 | Docker 볼륨 영속성 | 30분 |
| 7 | Git 및 VS Code 연동 마무리 | 25분 |
| 8 | README, 스크린샷, 최종 검토 | 50분 |
| 여유 | 오류 대응 및 재실행 | 40분 |
| 합계 |  | 5시간 |

## 1단계 — Docker 설치 및 점검

```bash
docker --version
docker info
```

확인할 내용:

- Docker 버전과 빌드 번호
- Docker Context가 `orbstack`인지
- Client와 Server 정보가 모두 출력되는지
- Docker CLI가 Docker 엔진과 통신하는지

완료 항목:

- Docker 실행 환경 확인
- Docker 버전 확인
- Docker 데몬 동작 확인
- Docker CLI와 데몬 연결 확인

## 2단계 — hello-world와 Docker 기본 운영

```bash
docker run hello-world
docker images
docker ps
docker ps -a

docker pull ubuntu
docker run -dit --name codyssey-ubuntu ubuntu bash
docker ps
docker exec codyssey-ubuntu ls
docker exec codyssey-ubuntu sh -c 'echo "Hello from Ubuntu container"'
docker stats --no-stream codyssey-ubuntu
```

`attach`는 컨테이너 종료 가능성이 있으므로 해당 단계에서 별도로 진행한다. 확인 후 컨테이너를 중지한다.

```bash
docker stop codyssey-ubuntu
docker ps
docker ps -a
```

완료 항목:

- 이미지 다운로드 및 목록 확인
- 컨테이너 실행, 중지, 목록 확인
- hello-world 실행
- Ubuntu 내부 명령 실행
- 컨테이너 리소스 확인
- `attach`와 `exec` 차이 확인

`docker logs`는 출력이 분명한 Nginx 컨테이너에서 확인한다.

## 3단계 — Dockerfile과 Nginx 이미지

파일 구성:

```text
mandatory/
├── Dockerfile
├── README.md
└── site/
    └── index.html
```

Dockerfile:

```dockerfile
FROM nginx:alpine

COPY site/index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

빌드:

```bash
cd mandatory
docker build -t first-built-image .
docker images
```

실행 및 접속:

```bash
docker run -d --name first-container -p 8080:80 first-built-image
docker ps
docker logs first-container
curl http://localhost:8080
```

브라우저에서 `http://localhost:8080`으로 접속하고 주소창과 웹 페이지 내용이 함께 보이도록 스크린샷을 촬영한다.

커스텀 포인트는 “Nginx 기본 페이지를 직접 만든 `site/index.html`로 교체했다”로 기록한다.

## 4단계 — Nginx 권한 문제 재현과 복구

파일 권한:

```bash
docker exec first-container ls -l /usr/share/nginx/html/index.html
curl -i http://localhost:8080

docker exec -u 0 first-container chmod 000 /usr/share/nginx/html/index.html
docker exec first-container ls -l /usr/share/nginx/html/index.html
curl -i http://localhost:8080

docker exec -u 0 first-container chmod 644 /usr/share/nginx/html/index.html
curl -i http://localhost:8080
```

디렉토리 권한:

```bash
docker exec first-container ls -ld /usr/share/nginx/html
docker exec -u 0 first-container chmod 600 /usr/share/nginx/html
docker exec first-container ls -ld /usr/share/nginx/html
curl -i http://localhost:8080

docker exec -u 0 first-container chmod 755 /usr/share/nginx/html
curl -i http://localhost:8080
```

확인할 내용:

- 파일의 읽기 권한이 Nginx 응답에 미치는 영향
- 디렉토리의 실행 권한이 내부 파일 접근에 미치는 영향
- 변경 전·후 권한
- `644`, `755`, `r/w/x`의 의미

OrbStack에서 예상한 권한 오류가 나타나지 않으면 결과를 꾸미지 않고 재현 방식을 조정한다.

## 5단계 — 바인드 마운트 반영

```bash
docker run -d \
  --name codyssey-bind \
  -p 8081:80 \
  -v "$PWD/site:/usr/share/nginx/html:ro" \
  nginx:alpine

cat site/index.html
curl http://localhost:8081

echo "<h1>I'm changed html file</h1>" > site/index.html
cat site/index.html
curl http://localhost:8081

echo "<h1>I'm html file</h1>" > site/index.html
curl http://localhost:8081
```

확인할 내용:

- 호스트 파일의 변경 전·후
- 컨테이너 응답에 변경이 즉시 반영되는지
- 최종 HTML이 원래 내용으로 복구됐는지

## 6단계 — Docker 볼륨 영속성

```bash
docker volume create codyssey-data
docker volume ls

docker run -d \
  --name codyssey-volume-1 \
  -v codyssey-data:/data \
  ubuntu sleep infinity

docker exec codyssey-volume-1 \
  sh -c 'echo "Persistent Docker data" > /data/message.txt'
docker exec codyssey-volume-1 cat /data/message.txt

docker rm -f codyssey-volume-1
docker ps -a

docker run -d \
  --name codyssey-volume-2 \
  -v codyssey-data:/data \
  ubuntu sleep infinity
docker exec codyssey-volume-2 cat /data/message.txt
```

확인할 내용:

- 첫 번째 컨테이너에서 데이터 작성
- 첫 번째 컨테이너 삭제
- 두 번째 컨테이너에서 같은 데이터 확인
- 컨테이너와 볼륨의 수명 차이

## 7단계 — Git 및 VS Code 연동 마무리

```bash
git config --list
git branch --show-current
git remote -v
git status
```

README에는 `user.name`, `user.email`, `init.defaultbranch=main`, 현재 브랜치와 원격 저장소 주소를 기록한다.

VS Code에서는 다음을 확인한다.

- GitHub 로그인 상태
- Source Control에 현재 저장소가 표시되는지
- GitHub에서 저장소에 접근할 수 있는지
- 토큰과 인증 코드가 보이지 않도록 스크린샷 촬영

## 8단계 — README와 최종 제출 점검

README에 다음 내용을 보완한다.

- 각 단계의 실제 명령과 핵심 출력
- 완료한 수행 체크리스트
- `r/w/x`, `644`, `755` 설명
- 이미지와 컨테이너 차이
- `attach`와 `exec` 차이
- 포트 매핑이 필요한 이유
- 바인드 마운트와 Docker 볼륨 차이
- Git과 GitHub의 역할 차이
- 재현 가능한 실행 절차
- 스크린샷 링크

최종 검사:

- 실제 수행하지 않은 결과가 없는지 확인
- 토큰, 비밀번호, 개인키, 인증 코드가 없는지 확인
- Markdown 렌더링 확인
- 저장소에서 검토 문서가 제외됐는지 확인
- Git 상태와 원격 저장소 동기화 확인
- 사용자 검토 후 커밋 및 푸시

## 보너스 판단

필수 작업과 최종 검토가 끝난 뒤 45분 이상 남았을 때만 Docker Compose 단일 서비스 실행을 시도한다. 시간이 부족하면 필수 과제의 README와 증거 품질을 우선한다.

## 바로 시작할 명령

```bash
docker --version
docker info
```
