FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir requests pymysql cryptography

COPY sookmissing_db.py .

CMD ["python", "sookmissing_db.py"]