import os
from settings import SITES_RESTORE

class Param():

    def __help(self):
        """ Muestra la lista de argumentos a pasar por terminal
        """
        info = """
    --help  Lista los argumentos disponibles.
    --sites Lista los sitios configurados.
    -i      Restauración interactiva.
    -s      Nombre del sitio restaurar.
    -src    Pasar los backups locales de manera explicita {'db':'path', 'code': 'path'}.
    -rsrc   Pasar los backups desde el servidor remoto de backups de manera explicita {'db':'path', 'code': 'path'}.
    -only   Solo restaura el objeto indicado (db, code ó img) úselo solo para backup remoto.
    -full   Asigne valor True para realizar una restauración completa (code, db e img).
    -szdb   Obtiene el backup remoto de base de datos de mayor tamaño creado en las últimas 24 horas.
        """
        print(info)

    def interactivePrompt(self):
        print('\t\t---\n  Site  \tDomain')
        self.list_sites()
        site = input('Escriba el nombre del sitio a restaurar: ')
        while site not in SITES_RESTORE.keys():
            site = input('Escriba el nombre del sitio a restaurar: ')
        print('\t\t---')
        objs = input('Escriba los objetos a restaurar (code,db,img) separados por coma. Ejemplo -> code,img: ')
        os.environ['-s'] = site
        os.environ['-objs'] = objs

        if 'db' in tuple(objs.split(',')):
            print('\t\t---')
            szdb = input('¿Descargar el backup de base de datos de mayor tamaño creado en las últimas 24 horas? (Y/n): ')
            if szdb.upper() == 'Y' or szdb == '':
                os.environ['-szdb'] = 'True'
        print('\t\t---')

    def set_params(self, str_params):
        """ Extrae los parámetros pasados por linea de comando
            y se asignan a variables de entorno con el nombre de flag

        Args:
            str_params (str): Cadena de parametros pasados por terminal
        """
        if len(str_params):
            for str_param in str_params:
                if str_param == '--help':
                    self.__help()
                    exit()

                if str_param == '--sites':
                    self.list_sites()
                    exit()

                if str_param == '-i':
                    self.interactivePrompt()
                    break

                if '=' in str_param:
                    index_sep = str_param.index('=')
                    flag = str_param[0:index_sep]
                    value = str_param[index_sep+1:len(str_param)]
                    os.environ[flag] = value
        
    def getObjects(self):
        """ Obtiene un listo de objetos a resturara ej: db, code, img

        Returns:
            [tuple]: Tupla con objetos a restaurar
        """
        if os.environ.get('-objs'):
            return tuple(os.environ.get('-objs').split(','))
        if os.environ.get('-src'):
            return tuple(eval(os.environ.get('-src')).keys())
        elif os.environ.get('-rsrc'):
            return tuple(eval(os.environ.get('-rsrc')).keys())
        else:
            if os.environ.get('-only'):
                return (os.environ.get('-only'),)
            if os.environ.get('-full'):
                return ('db', 'code', 'img')

            return ('db', 'code')
    
    def list_sites(self):
        for site in SITES_RESTORE.keys():
            domain = SITES_RESTORE[site]['LOCAL_SERVER']['SHOP_URL']
            print(f' * {site} => {domain}')