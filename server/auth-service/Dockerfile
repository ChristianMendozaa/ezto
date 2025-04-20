# Dockerfile
FROM python:3.12-slim

# Evita que Python cree archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema (opcional pero recomendado)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia archivos de requerimientos
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código al contenedor
COPY . .

# Expone el puerto (mismo que usarás en docker-compose o al correrlo manualmente)
EXPOSE 8000

# Comando por defecto para arrancar el microservicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
