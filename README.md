# ps17_restore
Automatización de restauración de backups de Prestashop 1.7.x.

Prerequisitos
--
* *Python3.8 o superior*. Para validar si está instalado Python o la versión, use el comando: python3 --version. Si no está instalado o tiene instalada la versión 2.x.x. Intente instalarlo con este comando: **sudo apt install python3**
* *pip3*. Se requiere para gestionar los paquetes de Python. Para validar si está instalado pip3 o la versión, use el comando: pip3 --version.  Si no está instalado. Intente instalarlo con este comando: **sudo apt install -y python3-pip**
* *Usar entorno virtual de Python* ( Recomendado ). Este requisito es opcional pero se recomienda usarlo. Use es este comando para instalarlo. sudo apt install -y python3-venv: **sudo apt install -y python3-venv**.
* *Configurar un sitio web local para el backup.* Este proyecto no creará los archivos de configuración de apache, nginx o cualquier otro servidor que use, ni tampoco la estructura de directorios donde se aloja su e-commerce. Lo que va a hacer es reemplazar el código fuente de su e-commerce en Prestashop 1.7.x y de igual manera lo hará con la base de datos.

Instalación
--
1. Clonar o descargar el respositorio en el directorio de su elección.
2. Ir al directorio raíz del proyecto: **cd ps17_restore**.
3. Crear entorno virtual de Python. **sudo python3 -m venv venv**. 
4. Activar entorno virtual. **source venv/bin/activate**. Puede desactivar este entono virtual cuando deje de usar el proyecto, para esto use el comando: **deactivate**.
5. Instalar paquetes de python que requiere este proyecto. **sudo pip3 install -r requirements.txt**.
6. Generar archivo settings.py. **cp __settings.py settings.py**. En este archivo se debe configurar los datos de su proyecto y base de datos local.
7. Generar archivo .env. **cp .env.sample .env**. Este archivo estará oculto en el explorador de archivos y se podrán definir variables de entorno con datos sensibles como la Ip del servidor en el cual se encuentran los backups, las rutas a los directorios de cada backup y datos de conexión a la base de datos local.
8. Restaurar backup. **sudo python3 restore.py**. Este comando va a restaurar el código fuente y base de datos. Las imágenes de productos no la va a restaurar, pero en caso que desee hacer una restauración que incluya imágenes de productos puede agregar el argumento "-full=True" de la siguiente manera: **sudo python3 restore.py -full=True**. Ahora simplemente hay que esperar a que se restaure el sitio.


Argumentos de línea  de comandos
--
**--help** => Lista los argumentos disponibles.

**-s** => Nombre del sitio restaurar.

**-src** => Pasar los backups locales de manera explicita {'db':'path', 'code': 'path'}.

**-rsrc** => Pasar los backups desde el servidor remoto de backups de manera explicita {'db':'name_file.tar.gz', 'code': 'name_file.tar.gz'}.

**-only** => Solo restaura el objeto indicado (db, code ó img) úselo solo para backup remoto.

**-full**  => Asigne valor True para realizar una restauración completa (code, db e img).

**-szdb**  =>  Obtiene el backup remoto de base de datos de mayor tamaño creado en las últimas 24 horas.

Uso de argumentos de línea de comandos
--
* ```sudo python3 restore.py -s=my_site```. El archivo settings.py permite configurar muchos sitios a restaurar en valor de **-s** hace referencia al sitio a restaurar y en concreto a la llave de configuración dentro de la variable "SITES_RESTORE". Cada llave corresponde a los datos de configuración de un sitio en específico.
* ```sudo python3 restore.py -src="{'db':'/home/user/backups/db/backup_db.tar.gz', 'code':'/home/user/backups/code/backup_code.tar.gz', 'img':'/home/user/backups/img/backup_img.tar.gz'}"```. Permite restaurar un sitio con backup locales, solo debe pasar un objeto json con el tipo de objeto a restaurar y la ruta donde está su backup. Todos los tipo de objetos son opcionales pero necesita pasar mínimo 1 por ejemplo si solo se quiere restaurar la base de datos el objeto json debe quedar así: "{'db':'/home/user/backups/db/backup_db.tar.gz'}".
* ```sudo python3 restore.py -rsrc="{'db':'backup_db.tar.gz', 'code':'backup_code.tar.gz', 'img':'backup_img.tar.gz'}"```. Funciona similar a "-src" pero en este caso buscará el archivo del backup en el servidor remoto de backups, solo se debe indicar en un objeto json en tipo de objeto y el nombre del backup a restaurar, la ruta de directorios de cada objeto a restaurar no es necesario ponerla ya que se ha definido en el archivo setting.py.
* ```sudo python3 restore.py -only=db```. Si solo desea restaurar un tipo de objeto indiquelo como valor del argumento "-only". En este ejemplo se indica que solo se requiere restaurar la base de datos.
* ```sudo python3 restore.py -full=True```. Restaura todos los tipos de objetos permitidos: db, code e img.
* ```sudo python3 restore.py -szdb=True```. Selecciona el backup de base da datos de mayor tamaño y que se haya creado en las últimas 24 horas. Úselo si está generando algunos backups que excluyen tablas y otros con todas las tablas. Puede ser combinado con el argumento "-only".
