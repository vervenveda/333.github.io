# syntax=docker/dockerfile:1

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN addgroup --system network333 \
    && adduser --system --ingroup network333 --home /app network333 \
    && mkdir -p /data/uploads \
    && chown -R network333:network333 /app /data

COPY requirements-runtime.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements-runtime.txt

COPY . .

USER network333

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)" || exit 1

CMD ["sh", "-c", "uvicorn ${APP_MODULE:-app.main:app} --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]
