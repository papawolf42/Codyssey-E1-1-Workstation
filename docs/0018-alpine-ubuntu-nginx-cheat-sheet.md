# Alpine · Ubuntu · Nginx 시험 치트시트
## 가장 중요한 구분
- **Ubuntu·Alpine = Linux 배포판(프로그램이 실행될 기반 환경)**
- **Nginx = 그 환경 위에서 실행되는 웹 서버 프로그램**
- Linux 배포판 = Linux 커널 주변에 명령어·라이브러리·패키지 관리자를 묶은 구성

## Ubuntu
- Debian 계열의 대중적인 Linux 배포판
- 장점: 사용 편의성, 풍부한 패키지·문서, 높은 호환성
- 패키지 관리자: `apt`
- 패키지 설치: `apt update && apt install curl`
- 컨테이너 진입: `docker run -it ubuntu bash`
- 비유: 기본 가구와 도구가 잘 갖춰진 넓은 집

## Alpine Linux
- 작고 단순하며 자원 효율적인 Linux 배포판
- `musl libc`, BusyBox를 중심으로 구성
- 패키지 관리자: `apk`
- 패키지 설치: `apk add --no-cache curl`
- 컨테이너 진입: `docker run -it alpine sh`
- 장점: 작은 이미지와 적은 기본 구성 요소
- 주의: 도구 부족이나 `musl` 호환성 문제가 생길 수 있어 항상 최선은 아님
- 비유: 꼭 필요한 시설만 갖춘 작고 효율적인 집

## Nginx
- 발음: **엔진 엑스(engine x)**
- HTTP 요청을 받아 HTML·CSS·이미지 같은 파일을 전달하는 웹 서버
- 요청을 뒤쪽 앱 서버로 전달하는 **리버스 프록시** 역할 가능
- 여러 서버로 요청을 나누는 **로드 밸런서** 역할 가능
- HTTP 기본 포트 `80`, HTTPS 기본 포트 `443`
- Nginx는 운영체제가 아니라 Ubuntu·Alpine 위에서 실행되는 프로그램

## `nginx:alpine`
- `nginx`는 이미지 이름, `alpine`은 태그
- 의미: **Alpine 기반 환경에 Nginx가 준비된 Docker 이미지 변형**
- `FROM nginx:alpine` = Nginx를 직접 설치하지 않고 준비된 이미지를 출발점으로 선택
- `COPY site/index.html ...` = 기본 웹 페이지를 내가 만든 HTML로 교체
- `EXPOSE 80` = 80번 포트 사용 예정 문서화, 실제 연결은 아님
- `-p 8080:80` = 호스트 8080을 컨테이너 Nginx의 80에 실제 연결
> 최종 암기: **Ubuntu는 편의성과 호환성, Alpine은 작은 크기와 단순성, Nginx는 웹 요청 처리, `nginx:alpine`은 Alpine 위에 Nginx가 준비된 이미지다.**
