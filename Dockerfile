# Imagen base
FROM python:3.12-slim

# Establecemos directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema si las necesitas (ej: psycopg2, etc)
RUN apt-get update && apt-get install -y gcc

# Copiamos e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente
COPY . .

# Exponemos el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para correr el servidor
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
