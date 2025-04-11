# Usa una imagen base ligera de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y luego instálalos
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación (el código del servidor de discovery)
COPY . .

# Expón el puerto 8000
EXPOSE 8000

# Comando para arrancar la aplicación con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
