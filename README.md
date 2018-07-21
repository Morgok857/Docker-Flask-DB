## Descripcion
Prueba de concepto para levantar Flask sobre docker.

Dentro del directorio Dockerfile se encuentran los archivos necesarios para generar el contenedor de Flask 

## Instalacion

# Configuracion de la Base de datos
Primero creamos el contendor con la imagen mas nueva de MariaDB con el comando:

*docker run -d -p 0.0.0.0:$PUERTO_EN_EXTERNO:3306 -v $STORAGE_SAVE:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=$PASSWORD --name $CONTAINER_NAME mariadb*

Variables reemplazar en el comando de Docker:
*$PUERTO_EN_EXTERNO = Puerto en tu equipo que se debe exponer.*
*$STORAGE_SAVE = Directorio en tu equipo que compartes con el contendor y donde se guardan los binario de la base de datos.*
*$CONTAINER_NAME = Nombre del contenedor*
*$PASSWORD = password para el usuario root (El usuario root tiene permitido conectarse de forma remota)*

Nos conectamos a la instancia y creamos la base de datos con el comando:

*create database db_Flask ;*

Creamos un usuario para Flask con:

*GRANT ALL PRIVILEGES ON db_Flask.* TO 'user_flask'@'%' IDENTIFIED BY 'YOURPASSWORD';*

# Configuracion de Flask

Ahora ingresamos al directorio donde clonamos el REPO e ingresamos al directorio scr.
Creamos el archivo de configuracion:

*cp config.py.template config.py*

Debemos indicar el string de conexion a la base de datos que creamos anteriormente y guardamos.


Ahora ingresamos al directorio Dockerfile y veremos los siguientes 2 archivos:
* Dockerfile
* requeriments.txt

El archivo Dockerfile contiene los comandos necesarios para generar un contenedor con python3 y Flask. En el archivo requeriments.exe se declaran las dependencias de python a instalar para dentro del contenedor.

Para construir la imagen usamos el comando:

*docker build --no-cache -t flask:0.4 .*

Para iniciar el contenedor usamos:

*docker run -d --name $CONTAINER_NAME -p $PORT:5000 -v $STORAGE_SAVE:/app:Z -t flask:0.4*

Variables reemplazar en el comando de Docker:
$CONTAINER_NAME = nombre con el que se identifica el contenedor*
*$PORT en el cual debe escuchar el contenedor*
*$STORAGE_SAVE = Directorio en tu equipo que compartes con el contendor y donde se alojan los archivos de Flask*



Finalmente ingresamos a la url http://$MY_IP:$port

Variables reemplazar:
*$MY_IP = ip del equipo con docker*
*$PORT = puerto donde escuchar el contenedor con Flask

En caso que decearamos ver el log producido por FLASK debemos recurrir al log de docker con el comando:

*docker logs $CONTAINER*

$CONTAINER es la ID del conenedor creado anteriormente
