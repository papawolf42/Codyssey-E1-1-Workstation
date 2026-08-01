# Alpine, Ubuntu, Nginx를 비전공자에게 설명하기

> 핵심 질문: 셋 다 프로그램 이름처럼 보이는데, 무엇이 다르고 어떤 관계일까?

## 1. 먼저 한 문장씩

- **Alpine Linux**: 필요한 것만 작게 담는 데 초점을 둔 가벼운 Linux 배포판
- **Ubuntu**: 사용 편의성과 풍부한 자료·패키지를 갖춘 대중적인 Linux 배포판
- **Nginx**: 웹 페이지를 전달하고 요청을 중계하는 웹 서버 프로그램

가장 중요한 구분:

```text
Alpine과 Ubuntu = 프로그램이 동작할 기반 환경
Nginx           = 그 환경 위에서 실행되는 프로그램
```

Windows에 비유하면:

```text
Ubuntu 또는 Alpine ≈ Windows 같은 운영 환경
Nginx              ≈ Windows 위에 설치하는 웹 서버 프로그램
```

단, Docker 컨테이너의 Alpine·Ubuntu 이미지는 일반 PC용 운영체제 전체보다 훨씬 단순한 사용자 공간을 제공하며 호스트의 Linux 커널을 공유한다.

---

## 2. 운영체제와 Linux 배포판부터 이해하기

### 운영체제란?

운영체제는 컴퓨터 자원과 프로그램 사이를 관리하는 기본 소프트웨어다.

```text
사용자
  │
애플리케이션
  │
운영체제
  │
CPU·메모리·디스크·네트워크
```

운영체제는 다음과 같은 일을 한다.

- CPU와 메모리 관리
- 파일과 디렉토리 관리
- 네트워크 통신 관리
- 사용자와 권한 관리
- 프로그램 실행 지원

대표적인 운영체제 계열에는 Windows, macOS, Linux 등이 있다.

### Linux는 하나의 완제품 이름인가?

엄밀하게 말하면 Linux는 중심부인 **커널(kernel)**의 이름이다. 커널은 CPU, 메모리, 저장 장치, 네트워크 같은 하드웨어 자원을 관리한다.

사람들이 실제로 사용할 수 있도록 Linux 커널에 다음 요소를 묶어 배포한 구성을 **Linux 배포판(distribution)**이라고 한다.

- 기본 명령어
- 시스템 라이브러리
- 패키지 관리자
- 설정 도구
- 설치 프로그램
- 선택된 응용 프로그램

```text
Linux 커널
    +
기본 명령·라이브러리
    +
패키지 관리자·설정 정책
    =
Linux 배포판
```

Ubuntu와 Alpine Linux는 서로 다른 Linux 배포판이다.

### 같은 Linux인데 왜 여러 종류가 있는가?

자동차도 같은 목적을 가지면서 경차, 승용차, 트럭으로 나뉜다. Linux 배포판도 목적과 선택이 다르다.

| 선택 요소 | 배포판마다 달라질 수 있는 것 |
|---|---|
| 기본 프로그램 | 처음부터 포함하는 명령과 도구 |
| 크기 | 최소 환경인지, 풍부한 기본 환경인지 |
| 패키지 관리자 | 프로그램 설치 명령과 저장소 |
| 라이브러리 | 프로그램이 의존하는 시스템 구성 |
| 업데이트 정책 | 배포 주기와 지원 기간 |
| 주 사용 목적 | 데스크톱, 서버, 컨테이너, 임베디드 등 |

---

## 3. Ubuntu란?

Ubuntu는 Debian을 기반으로 발전한 대중적인 Linux 배포판이다. Canonical과 커뮤니티가 개발하며 데스크톱, 서버, 클라우드 등 여러 환경에서 사용된다.

발음은 보통 “우분투”라고 한다.

### 비유

Ubuntu를 가구와 기본 도구가 비교적 잘 갖춰진 집에 비유할 수 있다.

```text
Ubuntu
≈ 입주자가 쓰기 편하도록
  기본 시설과 안내 자료가 잘 준비된 집
```

초보자가 필요한 정보를 찾기 쉽고, 다양한 프로그램을 설치하기 편하며, 서버와 개발 학습 자료가 많다.

### Ubuntu의 특징

- 비교적 사용하기 편하다.
- 이용자와 학습 자료가 많다.
- 설치할 수 있는 패키지가 풍부하다.
- 데스크톱, 서버, 클라우드에서 널리 쓰인다.
- 정기적인 일반 릴리스와 장기 지원 LTS 릴리스가 있다.
- Docker 학습에서 익숙한 Linux 명령을 연습하기 좋다.

### 패키지 관리자

Ubuntu에서는 주로 `apt`를 이용해 프로그램을 설치한다.

```bash
apt update
apt install curl
```

해석:

```text
apt update
→ 설치 가능한 프로그램 목록을 최신 상태로 갱신

apt install curl
→ curl 프로그램 설치
```

`apt`는 앱스토어에서 프로그램을 검색하고 설치하는 과정과 비슷한 역할을 터미널에서 수행한다.

### Docker에서 Ubuntu 실행

```bash
docker run -it ubuntu bash
```

각 부분:

```text
docker run  새 컨테이너 생성·실행
-i          표준 입력 유지
-t          가상 터미널 제공
ubuntu      Ubuntu 이미지 사용
bash        Bash 셸 실행
```

컨테이너 안에서:

```bash
ls
pwd
echo "Hello Ubuntu"
```

이 실습은 Ubuntu 기반의 격리된 Linux 사용자 공간에서 기본 명령을 실행하는 경험이다.

### Ubuntu가 적합한 경우

- Linux를 처음 배우는 경우
- 풍부한 문서와 예제가 필요한 경우
- 다양한 패키지를 쉽게 설치해야 하는 경우
- 개발·테스트 도구가 많은 환경이 필요한 경우
- 이미지 크기보다 호환성과 편의성이 더 중요한 경우

---

## 4. Alpine Linux란?

Alpine Linux는 작고 단순하며 자원 효율적인 구성을 지향하는 독립적인 Linux 배포판이다. 공식 소개에서는 보안, 단순성, 자원 효율성을 중요하게 설명한다.

발음은 보통 “알파인 리눅스”라고 한다.

### 비유

Alpine을 꼭 필요한 시설만 갖춘 작고 효율적인 집에 비유할 수 있다.

```text
Alpine
≈ 공간을 아끼기 위해
  꼭 필요한 시설부터 넣은 작은 집
```

처음부터 모든 도구가 들어 있지 않을 수 있지만, 필요한 것만 선택해서 추가할 수 있다.

### Alpine의 특징

- 기본 이미지가 작다.
- 불필요한 구성 요소를 줄이기 좋다.
- 자원 사용과 이미지 전송량을 줄이는 데 유리할 수 있다.
- `musl libc`와 BusyBox를 중심으로 구성된다.
- 자체 패키지 관리자인 `apk`를 사용한다.
- 작은 컨테이너 베이스 이미지로 자주 사용된다.

### BusyBox란?

일반적인 Linux에서는 여러 기본 명령이 각각 별도 프로그램으로 제공될 수 있다. BusyBox는 많은 기본 Unix 명령 기능을 하나의 작은 실행 파일에 모아 제공한다.

```text
일반적인 구성
ls 프로그램 + cp 프로그램 + mv 프로그램 + 여러 도구

BusyBox 중심 구성
하나의 작은 도구가 여러 명령 역할 제공
```

이러한 선택은 Alpine 환경을 작게 유지하는 데 도움을 준다.

### `musl libc`란?

프로그램은 파일, 메모리, 네트워크 같은 운영체제 기능을 사용하기 위해 기본 시스템 라이브러리에 의존한다.

Alpine은 흔히 다른 Linux 배포판에서 사용하는 `glibc` 대신 `musl libc`를 사용한다.

비전공자 관점에서는 다음 정도로 이해하면 된다.

```text
glibc와 musl
= Linux 프로그램과 시스템 사이에서
  기본 기능을 연결하는 서로 다른 계열의 라이브러리
```

이 차이 때문에 Ubuntu에서 실행되던 사전 컴파일 프로그램이 Alpine에서는 그대로 실행되지 않는 경우가 있다.

### 패키지 관리자

Alpine은 `apk`를 사용한다.

```bash
apk add --no-cache curl
```

해석:

```text
apk add
→ 패키지 설치

--no-cache
→ 패키지 목록 캐시를 이미지에 불필요하게 남기지 않음
```

### Docker에서 Alpine 실행

```bash
docker run -it alpine sh
```

Alpine의 최소 이미지에는 Bash가 기본으로 없을 수 있어 `bash` 대신 `sh`를 사용하는 경우가 많다.

```text
Ubuntu에서 흔한 셸: bash
Alpine 최소 이미지에서 흔한 셸: sh
```

### Alpine이 적합한 경우

- 작은 컨테이너 이미지가 중요한 경우
- 필요한 패키지가 Alpine에서 잘 지원되는 경우
- 구성 요소를 최소화하고 싶은 경우
- 호환성 차이를 이해하고 대응할 수 있는 경우

### 작다고 항상 더 좋은가?

아니다.

작은 이미지는 다음 장점이 있을 수 있다.

- 다운로드와 배포가 빨라질 수 있음
- 저장 공간 사용 감소
- 기본 포함 구성 요소 감소

하지만 다음 비용도 있을 수 있다.

- 필요한 도구가 빠져 있을 수 있음
- 문제 해결이 더 어려울 수 있음
- `musl`과 `glibc` 차이로 호환성 문제가 생길 수 있음
- 추가 설치 과정 때문에 Dockerfile이 복잡해질 수 있음

이미지는 무조건 작은 것을 고르는 것이 아니라 애플리케이션 호환성, 보안 업데이트, 운영 편의성까지 고려해 선택해야 한다.

---

## 5. Ubuntu와 Alpine 비교

| 항목 | Ubuntu | Alpine Linux |
|---|---|---|
| 종류 | Linux 배포판 | Linux 배포판 |
| 기반 | Debian 계열 | 독립 배포판 |
| 방향 | 편의성·호환성·폭넓은 활용 | 단순성·작은 크기·자원 효율 |
| 패키지 관리자 | `apt` | `apk` |
| 기본 C 라이브러리 | 주로 `glibc` | `musl libc` |
| 기본 도구 구성 | 상대적으로 풍부 | 최소화된 경우가 많음 |
| 컨테이너 셸 예 | `bash` | `sh` |
| 학습 자료 | 매우 풍부 | 목적 중심의 자료 필요 |
| 흔한 선택 이유 | 사용 편의와 호환성 | 작은 컨테이너 이미지 |

집 비유:

```text
Ubuntu
→ 기본 가구와 도구가 비교적 많이 준비된 넓은 집

Alpine
→ 꼭 필요한 것부터 선택해 넣는 작은 집
```

중요:

> Ubuntu가 좋은 배포판이고 Alpine이 나쁜 배포판이거나 그 반대인 것이 아니다. 목적에 맞는 기반을 선택하는 문제다.

---

## 6. Nginx란?

Nginx는 HTTP 웹 서버, 리버스 프록시, 콘텐츠 캐시, 로드 밸런서 등의 역할을 수행할 수 있는 서버 프로그램이다.

표기는 `nginx`, 발음은 공식적으로 “engine x”, 즉 “엔진 엑스”다.

### 가장 쉬운 설명

웹 브라우저가 웹 페이지를 요청하면 Nginx가 해당 파일이나 결과를 찾아 응답한다.

```text
브라우저                         Nginx
   │                              │
   │── index.html 주세요 ────────▶│
   │                              │ 파일 확인
   │◀── HTML 내용을 응답 ─────────│
```

식당에 비유하면:

```text
브라우저 = 손님
HTTP 요청 = 주문
Nginx = 주문을 받고 음식을 전달하는 직원
HTML·CSS·이미지 = 손님에게 전달할 음식
```

### 웹 서버란?

웹 서버는 브라우저 같은 클라이언트의 HTTP 요청을 받고 HTTP 응답을 보내는 프로그램이다.

요청:

```http
GET /index.html HTTP/1.1
Host: example.com
```

응답:

```http
HTTP/1.1 200 OK
Content-Type: text/html

<h1>Hello</h1>
```

Nginx는 기본적으로 80번 포트에서 HTTP 요청을 받을 수 있다. HTTPS를 구성하면 일반적으로 443번 포트를 사용한다.

### 정적 파일 제공

Nginx는 HTML, CSS, JavaScript, 이미지처럼 미리 만들어진 파일을 직접 전달할 수 있다.

```text
/usr/share/nginx/html/index.html
                 │
                 ▼
       http://localhost/
```

현재 과제에서 사용하는 기능이 이것이다.

### 리버스 프록시

Nginx가 요청을 직접 완성하지 않고 뒤쪽의 애플리케이션 서버에 전달할 수도 있다.

```text
사용자
  │
  │ HTTP/HTTPS 요청
  ▼
Nginx
  │
  │ 내부 요청 전달
  ▼
Node.js·Python·Java 애플리케이션
```

이를 **리버스 프록시(reverse proxy)**라고 한다.

Nginx는 앞에서 다음 작업을 담당할 수 있다.

- HTTPS 인증서와 TLS 처리
- 요청을 내부 애플리케이션으로 전달
- 정적 파일 제공
- 응답 캐싱
- 접근 로그 기록
- 여러 서버로 요청 분산

### 로드 밸런서

사용자가 많아 서버 한 대로 처리하기 어려우면 Nginx가 요청을 여러 서버에 나눠 줄 수 있다.

```text
                 ┌─▶ 앱 서버 1
사용자 ─▶ Nginx ─┼─▶ 앱 서버 2
                 └─▶ 앱 서버 3
```

이 역할을 **로드 밸런싱(load balancing)**이라고 한다.

### Nginx는 운영체제인가?

아니다.

```text
Ubuntu·Alpine = Linux 배포판, 기반 환경
Nginx         = 그 위에 설치해서 실행하는 웹 서버 프로그램
```

Ubuntu에도 Nginx를 설치할 수 있고 Alpine에도 Nginx를 설치할 수 있다.

```text
Ubuntu + Nginx
Alpine + Nginx
```

---

## 7. `nginx:alpine`은 무슨 뜻인가?

현재 Dockerfile:

```dockerfile
FROM nginx:alpine
```

`nginx:alpine`은 하나의 묶음 이름이다.

```text
nginx   : alpine
└─┬──┘    └─┬──┘
이미지 이름   태그
```

이 태그는 일반적으로 다음 의미로 이해할 수 있다.

> Alpine Linux 기반 환경에 Nginx가 설치·설정된 Nginx 이미지 변형을 사용한다.

구조:

```text
호스트 컴퓨터
└ Docker
   └ nginx:alpine 컨테이너
      ├ Alpine 기반 사용자 공간
      ├ Nginx 프로그램
      └ 웹 페이지 파일
```

집 비유:

```text
Alpine
= 작고 기본적인 집

Nginx
= 그 집 안에 설치한 웹 접수 창구

nginx:alpine 이미지
= 작은 집에 웹 접수 창구까지 설치해 둔 복제용 설계 결과
```

### 왜 직접 Alpine에 Nginx를 설치하지 않는가?

물론 다음처럼 직접 구성할 수도 있다.

```dockerfile
FROM alpine
RUN apk add --no-cache nginx
```

하지만 공식 Nginx 이미지를 사용하면 Nginx 실행에 필요한 기본 구성이 이미 준비되어 있어 간단하고 재현하기 쉽다.

현재 과제에서는 다음만 추가하면 된다.

```dockerfile
FROM nginx:alpine

COPY site/index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

```text
FROM
→ Nginx와 Alpine이 준비된 기존 이미지 선택

COPY
→ 우리가 만든 웹 페이지로 기본 페이지 교체

EXPOSE
→ 컨테이너가 80번 포트를 사용할 예정이라고 문서화
```

---

## 8. 현재 과제가 실행되는 전체 구조

```text
macOS 호스트
│
├ OrbStack
│ └ Docker 엔진
│    │
│    └ first-nginx-container
│       ├ Alpine 기반 환경
│       ├ Nginx
│       └ /usr/share/nginx/html/index.html
│
└ 브라우저 또는 curl
   └ http://localhost:8080
```

포트 흐름:

```text
브라우저
localhost:8080
      │
      │ Docker -p 8080:80
      ▼
컨테이너:80
      │
      ▼
Nginx
      │
      ▼
index.html 응답
```

실행 명령:

```bash
docker build -t first-built-image .

docker run -d \
  --name first-nginx-container \
  -p 8080:80 \
  first-built-image
```

각 이름:

```text
first-built-image
→ nginx:alpine을 기반으로 우리가 만든 이미지

first-nginx-container
→ first-built-image로 실제 실행한 컨테이너
```

---

## 9. 세 가지를 음식점으로 비유하기

```text
Ubuntu
→ 넓고 기본 설비와 도구가 많이 갖춰진 주방

Alpine
→ 필요한 설비만 갖춘 작고 효율적인 주방

Nginx
→ 손님의 주문을 받고 음식이나 안내물을 전달하는 접수 직원

Docker 이미지
→ 주방과 직원을 같은 상태로 복제할 수 있는 표준 매장 틀

Docker 컨테이너
→ 표준 틀로 실제 문을 연 각각의 매장
```

Alpine이나 Ubuntu 중 어느 주방을 선택하더라도 Nginx라는 직원을 배치할 수 있다. 다만 주방에 기본으로 준비된 도구와 설치 방법이 다르다.

---

## 10. 자주 하는 오해

### 오해 1: Alpine은 Nginx의 가벼운 버전이다

아니다. Alpine은 Linux 배포판이고 Nginx는 웹 서버 프로그램이다.

### 오해 2: Ubuntu와 Nginx는 경쟁 제품이다

아니다. 역할이 다르다. Ubuntu 위에서 Nginx를 실행할 수 있다.

### 오해 3: `nginx:alpine`은 프로그램 하나만 들어 있다

아니다. Nginx가 실행되기 위한 Alpine 기반 사용자 공간, 라이브러리, 설정 등이 함께 들어 있다.

### 오해 4: Alpine은 작으므로 항상 최고의 선택이다

아니다. 프로그램 호환성, 운영 편의성, 디버깅 도구, 팀 경험을 함께 고려해야 한다.

### 오해 5: Ubuntu 컨테이너는 완전한 Ubuntu 컴퓨터다

일반적인 컨테이너 이미지는 데스크톱 GUI를 포함한 완전한 PC 설치와 다르다. 필요한 사용자 공간을 제공하고 호스트의 Linux 커널을 공유한다.

### 오해 6: Nginx가 HTML을 작성한다

Nginx는 보통 준비된 HTML 파일을 전달한다. HTML 내용은 개발자가 작성한다.

### 오해 7: `EXPOSE 80`만 쓰면 브라우저 접속이 된다

아니다. `EXPOSE`는 포트를 문서화한다. 호스트에서 접속하려면 실행할 때 `-p 8080:80` 같은 실제 포트 매핑이 필요하다.

---

## 11. 시험 예상 질문과 모범 답안

### Ubuntu란 무엇인가?

> Ubuntu는 Debian 계열의 Linux 배포판으로, 사용 편의성과 풍부한 패키지·문서를 갖추고 데스크톱, 서버, 클라우드에서 널리 사용된다.

### Alpine Linux란 무엇인가?

> Alpine Linux는 단순성, 작은 크기, 자원 효율성을 지향하는 Linux 배포판이다. `musl libc`, BusyBox, `apk` 패키지 관리자를 사용하며 컨테이너의 가벼운 기반 이미지로 자주 선택된다.

### Nginx란 무엇인가?

> Nginx는 브라우저의 HTTP 요청을 받아 HTML 같은 정적 파일을 응답하거나, 요청을 뒤쪽 애플리케이션 서버로 전달하는 웹 서버·리버스 프록시 프로그램이다.

### Ubuntu와 Alpine의 공통점과 차이점은?

> 둘 다 Linux 배포판이다. Ubuntu는 편의성, 폭넓은 패키지와 호환성을 중시하고, Alpine은 작은 크기와 단순성, 자원 효율성을 중시한다. 패키지 관리자도 Ubuntu는 `apt`, Alpine은 `apk`를 사용한다.

### Alpine과 Nginx의 차이는?

> Alpine은 프로그램이 실행될 Linux 기반 환경이고 Nginx는 그 환경 위에서 실행되는 웹 서버 프로그램이다.

### `nginx:alpine`의 의미는?

> `nginx` 이미지의 Alpine 기반 변형을 뜻한다. Alpine 기반 사용자 공간에 Nginx가 실행 가능하도록 구성된 이미지다.

### 왜 과제에서 `nginx:alpine`을 사용하는가?

> Nginx가 이미 구성된 비교적 작은 Alpine 기반 이미지를 사용하면 웹 서버를 처음부터 설치하지 않고, 직접 만든 HTML만 복사해 간단하고 재현 가능한 커스텀 이미지를 만들 수 있기 때문이다.

### `apt`와 `apk`의 차이는?

> 둘 다 패키지를 설치·관리하는 도구지만 `apt`는 Ubuntu·Debian 계열에서, `apk`는 Alpine Linux에서 사용한다.

---

## 12. 최종 암기표

| 질문 | 한 줄 답 |
|---|---|
| Ubuntu는? | 사용하기 편하고 자료가 풍부한 Debian 계열 Linux 배포판 |
| Alpine은? | 작고 단순하며 자원 효율적인 Linux 배포판 |
| Nginx는? | HTTP 요청을 처리하는 웹 서버·리버스 프록시 프로그램 |
| `apt`는? | Ubuntu 계열 패키지 관리자 |
| `apk`는? | Alpine 패키지 관리자 |
| `nginx:alpine`은? | Alpine 기반으로 구성된 Nginx 이미지 변형 |
| 이미지란? | 컨테이너를 만드는 템플릿 |
| 컨테이너란? | 이미지로 만든 실행 인스턴스 |

```text
Ubuntu ─┐
        ├─ Linux 기반 환경
Alpine ─┘

Nginx
└ 그 기반 환경 위에서 실행되는 웹 서버

nginx:alpine
└ Alpine 기반 + Nginx 준비 완료
```

## 최종 한 문장

> Ubuntu와 Alpine은 프로그램이 살아갈 수 있는 서로 다른 Linux 배포판이고, Nginx는 그 환경 위에서 웹 요청을 받아 HTML을 전달하거나 다른 서버로 요청을 중계하는 웹 서버 프로그램이며, `nginx:alpine`은 Alpine 기반에 Nginx를 준비해 둔 Docker 이미지다.

## 기준 자료

- [Alpine Linux 공식 소개](https://alpinelinux.org/about/)
- [Ubuntu 프로젝트 공식 소개](https://ubuntu.com/about)
- [Nginx 공식 사이트](https://nginx.org/en/)
