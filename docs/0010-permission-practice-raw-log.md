# 권한 변경 실습 원본 로그

```console
$ docker ps --filter name=first-container
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                                     NAMES
1151eb88d156   first-built-image   "/docker-entrypoint.…"   14 minutes ago   Up 14 minutes   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   first-container

$ docker exec first-container ls -ld /usr/share/nginx/html
drwxr-xr-x    1 root     root          4096 Jul 29 22:14 /usr/share/nginx/html

$ docker exec first-container ls -l /usr/share/nginx/html/index.html
-rw-r--r--    1 root     root            23 Jul 29 05:37 /usr/share/nginx/html/index.html

$ curl -sS -o /dev/null -w 'INITIAL_HTTP=%{http_code}\n' http://localhost:8080/
INITIAL_HTTP=200

$ docker exec -it first-container /bin/sh
/ # cd /usr/share/nginx/html
/usr/share/nginx/html # pwd
/usr/share/nginx/html
/usr/share/nginx/html # ls -ld .
drwxr-xr-x    1 root     root          4096 Jul 29 22:14 .
/usr/share/nginx/html # ls -l index.html
-rw-r--r--    1 root     root            23 Jul 29 05:37 index.html
/usr/share/nginx/html # chmod 600 index.html
/usr/share/nginx/html # ls -l index.html
-rw-------    1 root     root            23 Jul 29 05:37 index.html
```

```console
$ curl -sS -i http://localhost:8080/ | sed -n '1p'
HTTP/1.1 403 Forbidden

$ docker logs --tail 2 first-container
2026/07/29 22:29:17 [error] 31#31: *3 open() "/usr/share/nginx/html/index.html" failed (13: Permission denied), client: 192.168.65.1, server: localhost, request: "GET / HTTP/1.1", host: "localhost:8080"
192.168.65.1 - - [29/Jul/2026:22:29:17 +0000] "GET / HTTP/1.1" 403 153 "-" "curl/8.7.1" "-"
```

```console
/usr/share/nginx/html # chmod 644 index.html
/usr/share/nginx/html # ls -l index.html
-rw-r--r--    1 root     root            23 Jul 29 05:37 index.html
```

```console
$ curl -sS -i http://localhost:8080/ | sed -n '1p'
HTTP/1.1 200 OK
```

```console
/usr/share/nginx/html # chmod 644 .
/usr/share/nginx/html # ls -ld .
drw-r--r--    1 root     root          4096 Jul 29 22:14 .
/usr/share/nginx/html # ls -l index.html
-rw-r--r--    1 root     root            23 Jul 29 05:37 index.html
```

```console
$ curl -sS -i http://localhost:8080/ | sed -n '1p'
HTTP/1.1 403 Forbidden

$ docker logs --tail 2 first-container
2026/07/29 22:29:35 [error] 34#34: *5 "/usr/share/nginx/html/index.html" is forbidden (13: Permission denied), client: 192.168.65.1, server: localhost, request: "GET / HTTP/1.1", host: "localhost:8080"
192.168.65.1 - - [29/Jul/2026:22:29:35 +0000] "GET / HTTP/1.1" 403 153 "-" "curl/8.7.1" "-"
```

```console
/usr/share/nginx/html # chmod 755 .
/usr/share/nginx/html # ls -ld .
drwxr-xr-x    1 root     root          4096 Jul 29 22:14 .
/usr/share/nginx/html # ls -l index.html
-rw-r--r--    1 root     root            23 Jul 29 05:37 index.html
/usr/share/nginx/html # exit
```

```console
$ curl -sS -i http://localhost:8080/ | sed -n '1p'
HTTP/1.1 200 OK

$ docker exec first-container ls -ld /usr/share/nginx/html
drwxr-xr-x    1 root     root          4096 Jul 29 22:14 /usr/share/nginx/html

$ docker exec first-container ls -l /usr/share/nginx/html/index.html
-rw-r--r--    1 root     root            23 Jul 29 05:37 /usr/share/nginx/html/index.html

$ git status --short --branch
## main...origin/main
```
