import os
from dotenv import load_dotenv

load_dotenv()

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__))
SEP = os.path.sep # -Linux /  -Windows \
TMP_DIR = f'{PATH_PROJECT}{SEP}tmp'
USER_OS = PATH_PROJECT.split(f'{SEP}')[2] # whoami

SITES_RESTORE = {
    'default': {
        # Datos de conexión servidor de backups
        'REMOTE_SERVER': {
            'HOST': os.getenv('REM0TE_HOST'),
            'PORT': os.getenv('REMOTE_PORT'),
            'FOLDER_CODE': os.getenv('REMOTE_FOLDER_CODE'),
            'FOLDER_DB': os.getenv('REMOTE_FOLDER_DB'),
            'FOLDER_IMG': os.getenv('REMOTE_FOLDER_IMG')
        },
        # Datos de servidor y proyecto local
        'LOCAL_SERVER': {
            'SHOP_URL': 'my-local-site.com',
            'ROOT_SITE': '/var/www/my-local-site.com/htdocs',
            'LOGS_DIR': '/var/www/my-local-site.com/logs',
            'ID_SHOP': 1, # si usa multitienda asigne el id del sitio a restaurar
            'DEFAULT_PRODUCT_IMG': 'https://i.imgur.com/ZCVn8I4.jpg',
            'NEW_COOKIE_KEY': os.environ.get('NEW_COOKIE_KEY')
        },
        # Datos de conexión a base de datos
        'LOCAL_DB': {
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'DATABASE': 'name_database',
            'PS_PREFIX': 'ps_',
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'
        },
        'MODULES': {
            # Módulos a desahabilitar: table: ps_module in column: name
            'disable': [
                #'name_module' 
            ],
            # Módulos a poner en modo sandbox: table: ps_configuration in column name 
            'sandbox': {
                'vars': [
                    #'MODULE_NAME_VAR_SANDBOX'
                ]
            }
        }
    }
    # Agregue aquí más sitios a restaurar
}