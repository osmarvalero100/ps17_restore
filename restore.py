import os
import sys
from getpass import getpass
from src.code import Code
from src.database import Database
from src.img import Img
from tools.param import Param
from tools.validate import Validate
from tools.utils import Utils


if __name__ == '__main__':
    param = Param()
    
    param.set_params(sys.argv[1:])
    objects = param.getObjects()

    if not os.environ.get('-src'):
        print('Login servidor de backups')
        os.environ['RS_USER'] = input('Usuario: ')
        os.environ['RS_PASS'] = getpass('Contraseña: ')
    
    validate = Validate()
    
    # Validar configuración
    if validate.all():
        if 'db' in objects:
            db = Database()
            db.restore()
        if 'code' in objects:
            code = Code()
            code.restore()
        if 'img' in objects:
            img = Img()
            img.restore()

        Utils.print_summary()