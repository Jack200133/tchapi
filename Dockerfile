FROM ubuntu:22.04

# Instalar las dependencias necesarias y Python 3.9
RUN apt-get update && apt-get install -y \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y \
    python3.9 python3.9-distutils wget curl

# Instalar pip para Python 3.9
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py

# Establecer el directorio de trabajo en /flask
WORKDIR /flask

# Copiar requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias de requirements.txt
RUN python3.9 -m pip install -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python3.9", "/flask/main.py"]
