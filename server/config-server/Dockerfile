FROM python:3.11-slim

# 1) Instala git antes de pip install
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Copia y instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copia el resto del código
COPY . .

# 4) Expone y arranca Uvicorn
EXPOSE 8888
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888"]

