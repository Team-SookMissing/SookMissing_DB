FROM python:3.9-slim

# 작업 폴더 설정
WORKDIR /app

# 필수 라이브러리 설치
#MySQL 8.0 접속 보안 에러 해결용
RUN pip install --no-cache-dir requests pymysql cryptography

# 파이썬 코드 복사
COPY sookmissing_db.py .

# 컨테이너 실행 시 작동할 명령어
# (환경변수 DB_HOST가 없으면 기본값으로 'mysql-service'를 사용하도록 설정하면 좋습니다)
CMD ["python", "sookmissing_db.py"]