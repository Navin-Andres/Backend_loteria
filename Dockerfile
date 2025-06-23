# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y el código
COPY requirements.txt .
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE $PORT

# Comando para ejecutar la aplicación
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:${PORT} app:app"]