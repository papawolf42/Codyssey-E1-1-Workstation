# Dockerfile 쉽게 이해하기: Windows에 한글과 Word 설치하기

> 이 문서는 Dockerfile을 처음 접하는 사람이 이미지·컨테이너·빌드의 관계를 쉽게 이해할 수 있도록 Windows PC 설정 과정에 비유한다.

## 먼저 주의

여기서 “Windows에 한글과 Word를 설치한다”는 내용은 **Dockerfile의 개념을 설명하기 위한 비유**다.

- 일반적인 `nginx:alpine`, `ubuntu` 이미지는 Linux 기반이다.
- Windows용 한글이나 Microsoft Word를 해당 Linux 이미지에 실제로 설치한다는 뜻이 아니다.
- Word와 한글은 라이선스, 설치 파일, 로그인, GUI 등의 조건도 확인해야 한다.
- 이 문서의 목적은 “컴퓨터 환경을 정해진 순서로 자동 구성한다”는 Dockerfile의 역할을 이해하는 것이다.

---

## 1. 새 컴퓨터를 매번 직접 설정한다면

새 Windows 컴퓨터를 받았다고 가정하자.

업무를 시작하려면 다음 작업을 해야 한다.

1. Windows를 설치한다.
2. 업데이트를 적용한다.
3. 한글을 설치한다.
4. Microsoft Word를 설치한다.
5. 회사 문서 양식과 글꼴을 복사한다.
6. 기본 작업 폴더를 만든다.
7. 프로그램의 초기 설정을 변경한다.
8. 모든 프로그램이 정상 실행되는지 확인한다.

컴퓨터가 한 대라면 직접 할 수 있다. 하지만 직원 100명의 컴퓨터를 모두 같은 상태로 만들어야 한다면 문제가 생긴다.

- 설치 순서를 빼먹을 수 있다.
- 사람마다 다른 버전을 설치할 수 있다.
- 필요한 파일을 잘못된 위치에 복사할 수 있다.
- 설정 결과가 컴퓨터마다 달라질 수 있다.
- 새 컴퓨터가 생길 때마다 처음부터 반복해야 한다.

이 과정을 텍스트 파일에 정확한 순서로 기록하고 자동 실행할 수 있다면 훨씬 재현하기 쉬워진다.

Dockerfile이 바로 이런 **자동 설치·환경 구성 설명서**와 비슷하다.

---

## 2. 비유로 보는 Docker 구조

| Docker 개념 | Windows 사무용 PC 비유 |
|---|---|
| Dockerfile | Windows와 프로그램을 설치하는 자동 구성 설명서 |
| 베이스 이미지 | Windows가 기본 설치된 초기 컴퓨터 |
| `FROM` | 어떤 Windows 기본 환경에서 시작할지 선택 |
| `RUN` | 설치 프로그램이나 설정 명령 실행 |
| `COPY` | 회사 양식·글꼴·설정 파일 복사 |
| `ENV` | 기본 언어·환경 이름 같은 환경 변수 설정 |
| `WORKDIR` | 기본 작업 폴더 지정 |
| `CMD` | 컴퓨터를 켰을 때 기본으로 실행할 프로그램 지정 |
| `docker build` | 설명서대로 설치를 끝낸 표준 컴퓨터 틀 제작 |
| Docker 이미지 | 한글·Word·설정이 준비된 표준 컴퓨터 템플릿 |
| `docker run` | 템플릿을 복제해 실제 사용 가능한 컴퓨터 한 대 실행 |
| 컨테이너 | 실행 중인 각각의 업무용 컴퓨터 |
| 레지스트리 | 완성된 표준 컴퓨터 템플릿을 보관·배포하는 창고 |

전체 관계:

```text
Dockerfile
설치 순서와 설정을 기록한 설명서
        │
        │ docker build
        ▼
Docker 이미지
설치가 끝난 표준 컴퓨터 템플릿
        │
        │ docker run
        ▼
Docker 컨테이너
템플릿으로 만든 실제 실행 환경
```

---

## 3. 가상의 Windows Dockerfile

다음 코드는 개념 설명을 위한 가상 예시다. 실제 한글·Word 설치 코드가 아니다.

```dockerfile
# 1. Windows가 설치된 기본 환경에서 시작
FROM windows-office-base:2026

# 2. 설치 파일을 이미지 안으로 복사
COPY installers/hangul-installer.exe C:/Installers/
COPY installers/word-installer.exe C:/Installers/

# 3. 프로그램 설치
RUN C:/Installers/hangul-installer.exe /silent
RUN C:/Installers/word-installer.exe /silent

# 4. 회사 문서 양식 복사
COPY company-templates/ C:/Office/Templates/

# 5. 기본 작업 폴더 지정
WORKDIR C:/Office/Documents

# 6. 환경 변수 설정
ENV OFFICE_LANGUAGE=ko-KR

# 7. 환경 실행 시 기본 프로그램 지정
CMD ["C:/Program Files/Office/Word.exe"]
```

이 파일을 사람이 읽으면 다음과 같이 해석할 수 있다.

> Windows 기본 환경을 준비하고, 한글과 Word 설치 파일을 넣어 두 프로그램을 설치한다. 회사 문서 양식을 복사하고 기본 작업 폴더와 언어를 설정한 뒤, 환경이 실행되면 Word를 기본 프로그램으로 시작한다.

---

## 4. Dockerfile 명령을 설치 과정으로 해석하기

### `FROM`: 어떤 컴퓨터에서 시작할까?

```dockerfile
FROM windows-office-base:2026
```

비유:

> 아무것도 없는 빈 철판에서 컴퓨터를 만들지 않고, Windows가 기본 설치된 컴퓨터에서 시작한다.

실제 Dockerfile:

```dockerfile
FROM nginx:alpine
```

의미:

> Alpine Linux 위에 Nginx가 준비된 기존 이미지를 출발점으로 사용한다.

`FROM`은 일반적으로 Dockerfile의 첫 번째 핵심 명령이다.

---

### `COPY`: 설치 파일과 회사 문서를 옮기자

```dockerfile
COPY company-templates/ C:/Office/Templates/
```

비유:

> 내 컴퓨터에 있는 회사 문서 양식을 새 업무용 컴퓨터 안의 지정 폴더로 복사한다.

현재 과제의 실제 예:

```dockerfile
COPY site/index.html /usr/share/nginx/html/index.html
```

의미:

> 호스트의 `site/index.html`을 이미지 안의 Nginx 기본 웹 문서 위치에 복사해 기본 페이지를 교체한다.

주의:

- `COPY`의 원본 파일은 빌드 컨텍스트 안에 있어야 한다.
- 이미지가 완성된 후 호스트 원본을 수정해도 기존 이미지 속 사본은 자동으로 바뀌지 않는다.
- 수정 내용을 이미지에 넣으려면 다시 빌드해야 한다.

---

### `RUN`: 설치 프로그램을 실행하자

```dockerfile
RUN C:/Installers/hangul-installer.exe /silent
```

비유:

> 이미지 제작 과정에서 한글 설치 프로그램을 실행한다.

Linux 이미지 예:

```dockerfile
RUN apk add --no-cache curl
```

의미:

> Alpine 기반 이미지를 만드는 도중 `curl` 패키지를 설치한다.

중요:

> `RUN`은 주로 **이미지를 빌드하는 동안** 실행된다.

---

### `WORKDIR`: 기본 작업 폴더를 정하자

```dockerfile
WORKDIR C:/Office/Documents
```

비유:

> 사용자가 업무를 시작할 기본 문서 폴더를 지정한다.

Linux 예:

```dockerfile
WORKDIR /app
```

이후의 `RUN`, `COPY`, `CMD` 같은 명령은 이 작업 디렉토리를 기준으로 동작할 수 있다.

---

### `ENV`: 기본 환경 설정을 저장하자

```dockerfile
ENV OFFICE_LANGUAGE=ko-KR
```

비유:

> 이 업무 환경의 기본 언어 설정을 한국어로 기록한다.

일반적인 예:

```dockerfile
ENV APP_ENV=production
```

애플리케이션은 `APP_ENV` 값을 읽어 개발 모드와 운영 모드 같은 동작을 구분할 수 있다.

---

### `CMD`: 컴퓨터가 켜지면 무엇을 실행할까?

```dockerfile
CMD ["C:/Program Files/Office/Word.exe"]
```

비유:

> 준비된 업무 환경을 실행할 때 Word를 기본 프로그램으로 시작한다.

컨테이너 예:

```dockerfile
CMD ["python", "app.py"]
```

의미:

> 컨테이너가 시작되면 기본적으로 `python app.py`를 실행한다.

`CMD`로 시작한 주 프로세스가 끝나면 컨테이너도 보통 종료된다.

---

## 5. `RUN`과 `CMD`의 차이

시험에서 자주 헷갈리는 부분이다.

| `RUN` | `CMD` |
|---|---|
| `docker build` 중 실행 | `docker run`으로 컨테이너를 시작할 때 실행 |
| 프로그램 설치·파일 생성 등 이미지 제작 | 서버·애플리케이션 같은 주 프로세스 실행 |
| 실행 결과가 이미지 레이어에 반영 | 컨테이너 실행 동작을 결정 |
| 여러 번 작성 가능 | 기본 실행 명령은 보통 마지막 유효 설정 사용 |

Windows 비유:

```text
RUN = 컴퓨터 템플릿을 제작하면서 Word를 설치
CMD = 완성된 컴퓨터를 켰을 때 Word를 실행
```

모범 답안:

> `RUN`은 이미지를 빌드하는 동안 설치나 설정 명령을 실행하고, `CMD`는 완성된 이미지로 컨테이너를 시작할 때 실행할 기본 명령을 정한다.

---

## 6. 빌드는 표준 컴퓨터 틀을 만드는 과정

가상의 Dockerfile을 빌드한다고 가정하자.

```bash
docker build -t korean-office-image .
```

각 부분의 의미:

```text
docker build
└ 설명서인 Dockerfile을 읽어 이미지 제작

-t korean-office-image
└ 완성된 이미지 이름을 korean-office-image로 지정

.
└ 현재 디렉토리를 빌드 컨텍스트로 사용
```

Windows 비유:

> 현재 폴더에 있는 설치 파일과 회사 양식을 사용해, 모든 설치와 설정이 끝난 `korean-office-image`라는 표준 컴퓨터 템플릿을 만든다.

현재 과제의 실제 명령:

```bash
cd mandatory
docker build -t first-built-image .
```

이 명령은 `mandatory/Dockerfile`을 이용해 `first-built-image`라는 Nginx 이미지를 만든다.

---

## 7. 이미지는 설치 완료된 표준 템플릿

이미지는 다음 내용을 포함할 수 있다.

- 베이스 운영 환경
- 설치된 프로그램
- 복사된 애플리케이션 파일
- 환경 변수
- 기본 작업 디렉토리
- 컨테이너 시작 명령

Windows 비유:

> Windows, 한글, Word, 회사 글꼴, 문서 양식과 기본 설정이 모두 들어간 표준 컴퓨터 복제 원본이다.

이미지 목록 확인:

```bash
docker images
```

이미지는 실행 중인 컴퓨터가 아니라 컨테이너를 만들기 위한 템플릿이다.

---

## 8. 컨테이너는 실제로 실행한 컴퓨터 한 대

이미지로 컨테이너를 실행한다.

```bash
docker run --name employee-01 korean-office-image
```

Windows 비유:

> 표준 컴퓨터 템플릿을 이용해 `employee-01`이 사용할 업무용 컴퓨터 한 대를 만든 뒤 실행한다.

같은 이미지에서 여러 컨테이너를 만들 수도 있다.

```bash
docker run --name employee-01 korean-office-image
docker run --name employee-02 korean-office-image
docker run --name employee-03 korean-office-image
```

```text
korean-office-image
표준 컴퓨터 템플릿
      │
      ├── employee-01 컨테이너
      ├── employee-02 컨테이너
      └── employee-03 컨테이너
```

각 컨테이너는 같은 이미지에서 출발하지만 서로 별개의 실행 환경이다.

---

## 9. 이미지와 컨테이너를 혼동하면 안 되는 이유

| 이미지 | 컨테이너 |
|---|---|
| 설치 완료된 표준 템플릿 | 템플릿으로 만든 실행 환경 |
| `docker build`로 생성 | `docker run`으로 생성·실행 |
| 하나의 이미지로 여러 컨테이너 생성 가능 | 각 컨테이너는 이름과 상태를 따로 가짐 |
| `docker images`로 확인 | `docker ps -a`로 확인 |

현재 과제:

```text
이미지 이름: first-built-image
컨테이너 이름: first-nginx-container
```

```bash
docker build -t first-built-image .

docker run -d \
  --name first-nginx-container \
  -p 8080:80 \
  first-built-image
```

`first-built-image`와 `first-nginx-container`는 같은 것이 아니다.

---

## 10. Docker 이미지 레이어

Dockerfile의 주요 명령은 이미지에 변경 단계를 쌓는다.

가상 예:

```dockerfile
FROM windows-office-base:2026
COPY installers/ C:/Installers/
RUN install-hangul
RUN install-word
COPY templates/ C:/Office/Templates/
```

개념적으로 보면:

```text
5층: 회사 문서 양식 추가
4층: Word 설치
3층: 한글 설치
2층: 설치 파일 복사
1층: Windows 기본 환경
```

이 각 변경 단계를 **레이어(layer)**라고 생각할 수 있다.

레이어의 장점:

- 변경되지 않은 단계는 빌드 캐시로 재사용할 수 있다.
- 같은 베이스 레이어를 여러 이미지가 공유할 수 있다.
- 변경된 지점 이후의 단계만 다시 실행할 수 있다.

예를 들어 회사 문서 양식만 바뀌었다면, 앞부분의 프로그램 설치 단계는 캐시를 재사용하고 마지막 `COPY` 단계부터 다시 처리할 수 있다.

---

## 11. Dockerfile 순서가 중요한 이유

다음 Dockerfile을 보자.

```dockerfile
FROM office-base
COPY frequently-changing-documents/ C:/Documents/
RUN install-very-large-program
```

문서가 조금만 바뀌어도 `COPY` 레이어가 달라지고, 그 뒤의 큰 프로그램 설치 단계까지 다시 실행될 수 있다.

변경 빈도가 낮은 작업을 먼저 두면 캐시 활용에 유리하다.

```dockerfile
FROM office-base
RUN install-very-large-program
COPY frequently-changing-documents/ C:/Documents/
```

일반 원칙:

```text
자주 바뀌지 않는 설치·설정
        ↓
자주 바뀌는 소스코드·문서 복사
```

단, 정확한 순서는 프로그램의 의존성과 보안 업데이트 요구도 함께 고려해야 한다.

---

## 12. `COPY`와 바인드 마운트의 차이

회사 문서 양식을 이미지에 `COPY`했다고 가정하자.

```dockerfile
COPY company-templates/ C:/Office/Templates/
```

이 파일은 **빌드 시점의 사본**이다. 호스트의 원본을 나중에 수정해도 이미 만들어진 이미지에는 자동으로 반영되지 않는다.

| `COPY` | 바인드 마운트 |
|---|---|
| 빌드할 때 이미지에 파일 포함 | 실행할 때 호스트 경로 연결 |
| 이미지 자체에 파일이 들어감 | 파일은 호스트에 존재 |
| 수정 후 이미지 재빌드 필요 | 호스트 수정이 즉시 보일 수 있음 |
| 배포할 파일 포함에 적합 | 개발 중 소스·설정 공유에 적합 |

Windows 비유:

```text
COPY
= 표준 컴퓨터를 만들 때 회사 양식을 복사해 넣음

바인드 마운트
= 실행 중인 컴퓨터에 회사의 공유 문서 폴더를 연결함
```

---

## 13. 이미지와 볼륨의 차이

Word로 작성한 사용자 문서를 컨테이너 내부에만 저장하면 컨테이너 삭제 시 사라질 수 있다.

사용자 문서는 프로그램 이미지가 아니라 별도 볼륨에 저장하는 편이 적절하다.

```text
이미지
├ 운영 환경
├ 프로그램
└ 기본 설정

볼륨
└ 사용자가 작성한 영속 데이터
```

Windows 비유:

```text
이미지 = Windows와 Word가 설치된 표준 PC 템플릿
볼륨   = PC를 교체해도 유지되는 별도 문서 저장 드라이브
```

컨테이너를 새로 만들어도 같은 볼륨을 연결하면 기존 데이터를 다시 사용할 수 있다.

---

## 14. 실제 과제 Dockerfile 해설

현재 과제의 Dockerfile:

```dockerfile
FROM nginx:alpine

COPY site/index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

Windows 설치 비유로 번역하면:

```text
FROM nginx:alpine
→ Nginx가 이미 설치된 가벼운 표준 컴퓨터를 준비한다.

COPY site/index.html ...
→ 회사가 만든 홈페이지 파일을 웹 서버의 기본 문서 위치에 복사한다.

EXPOSE 80
→ 이 컴퓨터의 웹 서비스가 80번 창구를 사용할 예정이라고 기록한다.
```

빌드와 실행:

```bash
docker build -t first-built-image .

docker run -d \
  --name first-nginx-container \
  -p 8080:80 \
  first-built-image
```

해석:

```text
docker build
→ 설치 설명서를 실행해 표준 Nginx 이미지 제작

docker run
→ 그 이미지로 실제 Nginx 컨테이너 생성·실행

-d
→ 백그라운드 실행

--name first-nginx-container
→ 실행 환경의 이름 지정

-p 8080:80
→ 호스트 8080번 창구를 컨테이너 80번 창구와 연결
```

---

## 15. Dockerfile이 필요한 이유

### 수동 설치

```text
사람이 설명서를 읽음
→ 직접 클릭하고 설치
→ 실수나 버전 차이 발생 가능
→ 다른 컴퓨터에서 다시 반복
```

### Dockerfile 사용

```text
설치·설정을 코드로 기록
→ docker build로 자동 실행
→ 같은 절차를 반복 가능
→ 이미지로 저장·공유
→ 필요한 만큼 컨테이너 실행
```

핵심 장점:

1. **재현성**: 같은 절차로 비슷한 환경을 다시 만들 수 있다.
2. **자동화**: 수동 설치 단계를 줄인다.
3. **문서화**: 어떤 베이스와 설정을 사용했는지 코드로 확인할 수 있다.
4. **배포 편의성**: 완성된 이미지를 다른 환경에서 실행할 수 있다.
5. **일관성**: 팀원마다 설치 방법이 달라지는 문제를 줄인다.

---

## 16. 자주 하는 오해

### 오해 1: Dockerfile이 실행 중인 서버다

아니다.

```text
Dockerfile = 설계도
이미지     = 설계도로 만든 템플릿
컨테이너   = 템플릿을 실제로 실행한 환경
```

### 오해 2: `docker build`가 컨테이너를 실행한다

아니다.

- `docker build`: 이미지를 만든다.
- `docker run`: 이미지로 컨테이너를 생성하고 실행한다.

### 오해 3: Dockerfile의 `EXPOSE 80`이 실제 포트를 연다

아니다.

- `EXPOSE 80`: 80번 포트 사용 예정 문서화
- `docker run -p 8080:80`: 실제 포트 연결

### 오해 4: 이미지와 컨테이너는 같은 것이다

아니다. 하나의 이미지로 여러 개의 독립된 컨테이너를 만들 수 있다.

### 오해 5: 컨테이너에 저장한 파일은 항상 유지된다

아니다. 중요한 데이터는 볼륨이나 적절한 외부 저장소를 사용해 컨테이너 생명주기와 분리해야 한다.

### 오해 6: Docker 컨테이너는 완전한 물리 컴퓨터다

아니다. 비유에서는 컴퓨터라고 표현했지만, 실제 컨테이너는 호스트 커널을 공유하며 격리된 프로세스로 동작한다. 일반적인 가상 머신보다 가볍고 빠르게 시작할 수 있다.

---

## 17. 시험 예상 질문과 모범 답안

### Dockerfile이란 무엇인가?

> Dockerfile은 베이스 이미지, 파일 복사, 프로그램 설치, 환경 설정, 기본 실행 명령 등 Docker 이미지 생성 절차를 순서대로 기록한 텍스트 파일이다.

### Dockerfile을 Windows 프로그램 설치에 비유해 설명하시오.

> Dockerfile은 새 Windows 컴퓨터에 한글과 Word를 설치하고 회사 양식과 환경 설정을 적용하는 자동 설치 설명서와 같다. `docker build`는 설명서대로 설치가 완료된 표준 컴퓨터 템플릿인 이미지를 만드는 과정이고, `docker run`은 그 템플릿으로 실제 사용 가능한 실행 환경인 컨테이너를 만드는 과정이다.

### `FROM`의 역할은?

> 이미지 제작의 출발점이 되는 베이스 이미지를 지정한다. Windows 비유에서는 운영체제가 기본 설치된 컴퓨터를 선택하는 것과 같다.

### `COPY`의 역할은?

> 빌드 컨텍스트의 파일을 이미지 내부 경로로 복사한다. Windows 비유에서는 설치 파일이나 회사 문서 양식을 표준 컴퓨터에 복사하는 것과 같다.

### `RUN`과 `CMD`의 차이는?

> `RUN`은 이미지를 빌드할 때 프로그램 설치나 설정을 수행하고, `CMD`는 완성된 이미지로 컨테이너를 실행할 때 시작할 기본 명령을 지정한다.

### 이미지와 컨테이너의 차이는?

> 이미지는 프로그램과 설정이 준비된 템플릿이고, 컨테이너는 그 이미지를 바탕으로 생성된 실제 실행 인스턴스다. 하나의 이미지로 여러 컨테이너를 만들 수 있다.

### Dockerfile이 재현성에 도움이 되는 이유는?

> 사람이 수동으로 설치하는 대신 베이스 이미지와 설치·설정 절차를 코드로 기록하므로, 같은 Dockerfile을 이용해 여러 환경에서 동일한 절차를 반복할 수 있기 때문이다.

---

## 18. 최종 암기 그림

```text
새 Windows PC를 업무용으로 준비한다고 생각하자.

FROM
└ Windows가 설치된 기본 PC 선택

COPY
└ 한글·Word 설치 파일과 회사 양식 복사

RUN
└ 한글·Word 설치와 시스템 설정 수행

WORKDIR
└ 기본 문서 작업 폴더 지정

ENV
└ 언어·업무 환경 설정

CMD
└ PC를 켰을 때 기본 실행할 프로그램 지정

docker build
└ 위 설명대로 설치된 표준 PC 템플릿 제작

이미지
└ 설치가 완료된 복제 원본

docker run
└ 복제 원본으로 실제 업무 환경 실행

컨테이너
└ 현재 실행 중인 각각의 업무 환경
```

## 최종 한 문장

> Dockerfile은 새 컴퓨터에 운영 환경과 프로그램을 정해진 순서로 설치하고 설정하는 자동 설명서이며, `docker build`는 그 설명서로 이미지라는 표준 템플릿을 만들고 `docker run`은 이미지로 컨테이너라는 실제 실행 환경을 만드는 과정이다.
