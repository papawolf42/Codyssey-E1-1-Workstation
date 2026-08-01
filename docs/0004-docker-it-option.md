# Docker `-it` 옵션

## 기본 명령

```bash
docker run -it ubuntu bash
```

`-it`는 `-i`와 `-t`를 합쳐 쓴 옵션이다.

## `-i`

`--interactive`의 줄임말이다.

컨테이너의 표준 입력을 열어 둬서 사용자가 키보드로 명령을 입력할 수 있게 한다.

```bash
docker run -i ubuntu bash
```

입력은 가능하지만 일반 터미널처럼 화면이 표시되지 않을 수 있다.

## `-t`

`--tty`의 줄임말이다.

컨테이너에 가상 터미널을 할당한다. 셸 프롬프트, 줄바꿈, 키보드 입력 등이 일반 터미널처럼 동작하도록 만든다.

```bash
docker run -t ubuntu bash
```

터미널 화면은 만들어지지만 `-i`가 없으면 사용자의 입력을 계속 받을 수 없다.

## `-it`

두 옵션을 함께 사용하면 컨테이너 내부 셸을 일반 터미널처럼 조작할 수 있다.

```bash
docker run -it ubuntu bash
```

명령을 실행하면 다음과 같은 프롬프트가 나타난다.

```console
root@<container-id>:/#
```

이 시점부터 입력하는 `pwd`, `ls`, `echo` 같은 명령은 macOS 호스트가 아니라 Ubuntu 컨테이너 내부에서 실행된다.

## `exit`를 입력하면

```bash
exit
```

`docker run -it ubuntu bash`에서는 `bash`가 컨테이너의 메인 프로세스다. `exit`로 `bash`가 종료되면 컨테이너도 함께 종료되어 `Exited` 상태가 된다.

호스트에서 다음 명령으로 확인할 수 있다.

```bash
docker ps
docker ps -a
```

- `docker ps`: 종료된 컨테이너가 보이지 않는다.
- `docker ps -a`: 종료된 컨테이너까지 표시한다.

## `-dit`와의 차이

```bash
docker run -dit ubuntu bash
```

`-d`는 `--detach`의 줄임말로 컨테이너를 백그라운드에서 실행한다.

- `-it`: 컨테이너 내부 셸에 바로 연결한다.
- `-dit`: 입력과 가상 터미널을 유지하면서 컨테이너는 백그라운드에서 실행한다.

`-dit`로 실행한 컨테이너에는 나중에 `docker exec` 또는 `docker attach`로 접근할 수 있다.
