import os

class Param():

    def __help(self):
        """ Muestra la lista de argumentos a pasar por terminal
        """
        info = """
    --help  Lista los argumentos disponibles.
    -s      Nombre del sitio restaurar.
    -src    Pasar los backups locales de manera explicita {'db':'path', 'code': 'path'}.
    -rsrc   Pasar los backups desde el servidor remoto de backups de manera explicita {'db':'path', 'code': 'path'}.
    -only   Solo restaura el objeto indicado (db, code ó img) úselo solo para backup remoto.
    -full   Asigne valor True para realizar una restauración completa (code, db e img).
    -szdb   Obtiene el backup remoto de base de datos de mayor tamaño creado en las últimas 24 horas.
        """
        print(info)


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