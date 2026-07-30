# 0006. 시험 대비 KEYWORD CHEAT SHEET

> **5분 복습용:** 키워드를 보고 `정의 → 명령 → 증거`를 말할 수 있으면 된다.
> 기술 근거는 `instruction.md`, 당일 운영 근거는 `mail.txt`다. 과제 예시값은 시험 조건이 아니다.
> 상세 개념은 [0001](./0001-시험-대비-정리.md), 실습은 [0004](./0004-동료평가표-OCR-예상문답-실습로그.md), 당일 행동은 [0005](./0005-시험-당일-운영-주의사항.md)를 본다.

## 0. P0 — 당일 운영

| 키워드 | 행동 |
|---|---|
| `08:00 전` | 중요 파일 백업 |
| `개인 배정 장소` | 메일·문자로 확인하고 공개 문서에 쓰지 않기 |
| `09:40` | 도착 권장 |
| `10:00:00` | 입실 가능 마지막 시각 |
| `10:00:01` | 입실 불가 |
| `자리 이탈` | 화장실 포함 즉시 시험 종료 |
| `전자기기` | 작동·울림 발생 시 즉시 퇴실 |
| `시험용 iMac 계정` | 제공 계정 사용, 개인 계정 사용 불가 |
| `한/영 전환` | 로그인 직후 설정·확인 |
| `A4 1장 + 펜` | 운영진 배부품 사용 후 반납 |
| `[종료]` | 완료 후 직접 클릭 |
| `13:00` | 미클릭 시 그 시점 점수로 자동 처리 |
| `퇴장 서명` | 반납 후 퇴장할 때 서명 |

## 1. P1 — 공식 과제 기반 핵심

| 키워드 | 한 줄 답 |
|---|---|
| `절대 경로` | `/`부터 시작, 현재 위치와 무관 |
| `상대 경로` | 현재 작업 디렉터리 기준 |
| `r / w / x` | 읽기 `4` / 쓰기 `2` / 실행·진입 `1` |
| `755` | `rwxr-xr-x` |
| `644` | `rw-r--r--` |
| `이미지` | 컨테이너를 만드는 읽기 전용 템플릿 |
| `컨테이너` | 이미지에서 실행된 격리 프로세스 |
| `Dockerfile` | 이미지를 재현 가능하게 만드는 빌드 명세 |
| `build / run` | 이미지 생성 / 컨테이너 생성·실행 |
| `FROM / RUN / COPY` | 기반 이미지 / 빌드 명령 / 파일 복사 |
| `CMD / ENTRYPOINT` | 시작 시 실행할 기본 명령 |
| `EXPOSE / -p` | 포트 설명 / 실제 호스트 공개 |
| `-p H:C` | 호스트 `H` → 컨테이너 `C` |
| `-d / -it / --rm` | 백그라운드 / 대화형 / 종료 시 자동 삭제 |
| `attach / exec` | 메인 프로세스 연결 / 새 프로세스 실행 |
| `포트 충돌` | 호스트 포트를 다른 프로세스·컨테이너가 점유 |
| `바인드 마운트` | 지정한 호스트 경로 직접 연결 |
| `볼륨` | Docker가 관리하는 영속 저장소 |
| `영속성` | 컨테이너를 삭제·재생성해도 데이터 유지 |
| `Git / GitHub` | 로컬 버전 관리 / 원격 저장·협업 |
| `commit / push` | 로컬 이력 / 원격 전송 |
| `민감정보` | 커밋 금지; 노출 시 폐기·재발급 |

`Compose · 환경 변수 활용 · GitHub SSH`는 공식 문서에서 **선택 보너스**다.

## 2. P1 — 명령 복원 카드

```bash
# 경로·파일·권한
pwd
ls -la
mkdir -p DIR
touch FILE
cp SOURCE DEST
mv SOURCE DEST
rm FILE
chmod 644 FILE
chmod 755 DIR
stat -f '%Sp %OLp %N' FILE DIR       # macOS

# Docker 상태·수명주기
docker --version
docker info
docker run --rm hello-world
docker pull IMAGE
docker images
docker ps
docker ps -a
docker logs CONTAINER
docker stats --no-stream CONTAINER
docker exec -it CONTAINER sh
docker attach CONTAINER               # 분리: Ctrl-p, Ctrl-q
docker stop CONTAINER
docker rm CONTAINER

# 빌드·포트·접속
docker build -t IMAGE .
docker run -d --name CONTAINER -p 127.0.0.1:HOST_PORT:CONTAINER_PORT IMAGE
docker port CONTAINER
curl -i http://127.0.0.1:HOST_PORT

# 충돌 확인
docker ps --format 'table {{.Names}}\t{{.Ports}}'
lsof -nP -iTCP:HOST_PORT -sTCP:LISTEN

# 볼륨 영속성
docker volume create VOLUME
docker run --rm -v VOLUME:/data IMAGE sh -c 'echo saved > /data/check.txt'
docker run --rm -v VOLUME:/data IMAGE cat /data/check.txt

# Git
git config --list
git status
git diff
git add FILE
git diff --cached
git commit -m "MESSAGE"
git remote -v
git push
```

대문자 이름은 문제 조건에 맞게 바꾼다. 성공은 `ps · port · curl · logs · 재조회` 중 맞는 증거로 확인한다.

## 3. 유력 질문 → 답 키워드

| 질문 | 답 키워드 |
|---|---|
| 절대/상대 경로? | `기준점 · 현재 위치 · 이동성` |
| `755`/`644`? | `4·2·1 · user/group/others · 디렉터리 x=진입` |
| 이미지/컨테이너? | `템플릿 · 실행 인스턴스 · writable layer` |
| 포트 매핑 이유? | `네트워크 격리 · H:C · EXPOSE≠공개` |
| 포트 충돌 대응? | `오류 → docker ps/port → lsof → 조치 → curl/logs` |
| 볼륨이 필요한 이유? | `데이터 수명 분리 · 삭제 · 재연결 · 재조회` |
| 볼륨/바인드? | `Docker 관리 · 호스트 경로 · 이식성` |
| Git/GitHub? | `로컬 이력 · 원격 협업 · commit≠push` |
| attach/exec? | `PID 1 입출력 · 새 프로세스 · 종료 신호` |
| 문제 해결 설명? | `현상 · 가설 · 확인 · 최소 조치 · 재검증` |

## 4. 답변 공식

- 개념형: `정의 → 왜 필요한가 → 대표 명령 → 출력에서 본 증거`
- 장애형: `현상 → 가설 → 확인 명령 → 최소 조치 → 같은 기준으로 재검증`
- 금지형: `그냥 재설치 · 아마 성공 · 명령만 나열 · 확인 없는 성공 선언`

## 5. 미확정 — 외우지 말 것

- 문항 수·형식·배점·합격 기준
- 인터넷·검색·외부 AI·개인 노트 허용 여부
- 특정 포트·파일명·이미지명·컨테이너명·HTML 출력
- Docker Compose·GitHub SSH의 실제 출제 여부
- `주관식 · 10~15문항 · 힌트 제공` 루머

## 마지막 20초

`r=4 w=2 x=1` · `755/644` · `image/container` · `H:C` · `EXPOSE≠-p` · `bind/volume` · `commit/push`
`오류 원문 → 가설 → 확인 → 최소 조치 → 재검증` · `자리 이탈 금지` · `전자기기 작동·울림 차단` · `[종료]`
