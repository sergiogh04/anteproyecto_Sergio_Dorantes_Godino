# Dockerfile
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependencias
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Crea directorio
WORKDIR /app

# Copia los archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto y ejecuta
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
