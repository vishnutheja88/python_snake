# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=80

WORKDIR /app

# Install tini for proper signal handling and ca-certificates for HTTPS
RUN apt-get update \
 && apt-get install -y --no-install-recommends tini ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app/ ./app

# Install Python dependencies
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir flask gunicorn

# Create an unprivileged user and fix ownership
RUN groupadd --system appgroup \
 && useradd --system --gid appgroup --home-dir /nonexistent --no-create-home --shell /usr/sbin/nologin appuser \
 && chown -R appuser:appgroup /app

EXPOSE 80

USER appuser

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app.app:app", "--workers", "2", "--threads", "4"]
