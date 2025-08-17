FROM python:3.10-slim

RUN useradd -m appuser
WORKDIR /app

RUN apt-get update && apt-get install -y \
    sqlite3 gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Tạo thư mục DB + ảnh trong container
RUN mkdir -p /app/instance /app/app/static/images && \
    chown -R appuser:appuser /app

USER appuser
EXPOSE 8080
CMD [ "sh", "-c", "python init_db.py && python main.py" ]
