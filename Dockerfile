FROM python:3.10-slim

# Instalar dependencias del sistema incluyendo locale
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    chromium-driver \
    chromium \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Configurar locale en español
RUN sed -i 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

# Variables de entorno para Chrome headless y locale español
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    LANG=es_ES.UTF-8 \
    LC_ALL=es_ES.UTF-8 \
    LC_TIME=es_ES.UTF-8

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo del bot de piquetes y el archivo .env
COPY piquete_alerta.py .
COPY .env .

# Comando específico para el bot de piquetes
CMD ["python", "piquete_alerta.py"]
