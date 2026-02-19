FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* /app/
RUN uv sync --no-dev

COPY . /app
COPY scripts /app/scripts
RUN chmod +x /app/scripts/run.sh

CMD ["/app/scripts/run.sh"]
