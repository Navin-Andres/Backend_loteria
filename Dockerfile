# Usa una imagen base de Python slim para un entorno ligero
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias del sistema necesarias para compilar pandas
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar la aplicación usando la variable de entorno PORT
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT} app:app"]