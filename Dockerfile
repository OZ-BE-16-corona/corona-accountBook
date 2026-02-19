FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* /app/

# prod 그룹 설치 (프로젝트 venv에 설치됨)
RUN uv sync --no-dev

COPY . /app

EXPOSE 8000
