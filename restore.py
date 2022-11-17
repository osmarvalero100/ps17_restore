import os
import sys
import time
from getpass import getpass
from multiprocessing import Pool
from src.code import Code
from src.database import Database
from src.img import Img
from tools.param import Param
from tools.validate import Validate
from tools.utils import Utils
from tools.ssh import Ssh

def download(type_obj):
    dw_path_file = Ssh().scp_file_download(type_obj)
    print(f"{type_obj}[ Descargado en: {dw_path_file} ]")

def restore(obj):
    if 'db' == obj:
        db = Database()
        db.restore()
    if 'code' == obj:
        code = Code()
        code.restore()
    if 'img' == obj:
        img = Img()
        img.restore()

if __name__ == '__main__':
    param = Param()
    param.set_params(sys.argv[1:])
    objects = param.getObjects()

    if not os.environ.get('-src'):
        print('Login servidor de backups')
        os.environ['RS_USER'] = input('Usuario: ')
        os.environ['RS_PASS'] = getpass('Contraseña: ')
    
    if os.environ.get('-dw', '') != '':
        dw_objects = os.environ.get('-dw')
        dw_objects = tuple(map(str, dw_objects.split(',')))
        if 'db' in dw_objects:
            szdb = input('¿Descargar el backup de base de datos de mayor tamaño creado en las últimas 24 horas? (Y/n): ')
            if szdb.upper() == 'Y' or szdb == '':
                os.environ['-szdb'] = 'True'
        Pool().map(download, dw_objects)
        exit()
    
    validate = Validate()
    os.environ['restore_objects'] = ','.join(objects)
    # Validar configuración
    if validate.all():
        os.environ['start_time_bk'] = str(time.time())
        Pool().map(restore, objects)
        Utils.print_summary()
        