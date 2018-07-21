FROM ubuntu:16.04
MAINTAINER Morgok
# Instala los paquetes base
RUN apt-get update -y
RUN apt-get install -y apt-utils python3-pip python3-dev build-essential mysql-client libmysqlclient-dev
# Incluye el archivo de las depencencias a instalar
ADD requeriments.txt /root/requeriments.txt
# Configura el directorio raiz para la aplicacion
WORKDIR /app
# actualiza pip3 e instala las dependencia
RUN pip3 install --upgrade pip
RUN pip3 install -r /root/requeriments.txt
# Inicia el archivo principar de Flask. Si este proceso de detiene el contenedor se detiene
ENTRYPOINT ["python3"]
CMD ["main.py"]
