# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de la aplicación en el contenedor
COPY . /app

# Instala las dependencias necesarias
#RUN pip install pyTelegramBotAPI

RUN pip install python-telegram-bot



# Comando para ejecutar el bot
CMD ["python", "finanzas_personales.py"]
