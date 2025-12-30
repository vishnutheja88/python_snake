FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY app/ ./app
RUN pip install --no-cache-dir flask gunicorn
EXPOSE 80
# run the Flask app via gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:80", "app.app:app", "--workers", "2", "--threads", "4"]
