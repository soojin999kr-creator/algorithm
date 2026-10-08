# 파이썬 3.11 슬림 이미지를 기반으로 작성
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 파이썬 패키지 버퍼링 방지 설정
ENV PYTHONUNBUFFERED=1

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run은 PORT 환경변수를 주입함 (기본값 8080)
ENV PORT=8080

# uvicorn 서버 실행 명령어 (Cloud Run 포트 바인딩 대응)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
