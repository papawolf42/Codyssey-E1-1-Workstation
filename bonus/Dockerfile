# 가벼운 Python 3.12 이미지를 사용한다.
FROM python:3.12-slim

# 컨테이너 안의 작업 폴더를 지정한다.
WORKDIR /app

# 앱의 기본 실행 모드를 환경변수로 지정한다.
ENV APP_MODE=normal

# 필요한 Python 패키지를 먼저 설치한다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Flask 앱을 컨테이너에 복사한다.
COPY app.py seed.py ./

# Flask 앱이 사용하는 컨테이너 내부 포트다.
EXPOSE 5000

# 테스트 계정을 준비한 뒤 Flask 앱을 실행한다.
CMD ["sh", "-c", "python seed.py && python app.py"]
