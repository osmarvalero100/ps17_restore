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
    os.environ['start_time_bk'] = str(time.time())
    param = Param()
    param.set_params(sys.argv[1:])
    objects = param.getObjects()

    if not os.environ.get('-src'):
        print('Login servidor de backups')
        os.environ['RS_USER'] = input('Usuario: ')
        os.environ['RS_PASS'] = getpass('Contraseña: ')
    
    validate = Validate()
    os.environ['restore_objects'] = ','.join(objects)
    # Validar configuración
    if validate.all():
        Pool().map(restore, objects)
        Utils.print_summary()
        