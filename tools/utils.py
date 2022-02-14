import os
import json
from settings import TMP_DIR, SEP
from .cmd import Cmd

class Utils():
    """
    Métodos utiles de uso general
    """

    @staticmethod
    def get_file_size(path_bk):
        """Obtiene el peso de un archivo

        Args:
            path_bk (str): Ruta del archivo

        Returns:
            [str]: Peso archivo
        """
        cmd = Cmd()

        try:
            command = [f'du -csh {path_bk} | grep total']
            result = cmd.execute(command)

            return result.replace('total', '').rstrip()
        except Exception as e:
            return '--'

    @staticmethod
    def get_tmp_path_site_by_object(obj_type):
        """
        Args:
            obj_type (str): db - code - img
        
        returns:
            [str]: Ruta temporal donde se almacena el tipo de objeto
        """
        site = os.environ.get('-s', 'default')

        return f'{TMP_DIR}{SEP}{site}{SEP}{obj_type}'

    
    @staticmethod
    def get_summary():
        site = os.environ.get('-s', 'default')
        summary_json = f'{TMP_DIR}{os.path.sep}{site}.json'

        if not os.path.isfile(summary_json):
            return {
                'code': {},
                'db': {},
                'img': {},
            }

        try:
            with open(summary_json) as summary:
                return json.load(summary)
        except json.decoder.JSONDecodeError as e:
            return []

    @staticmethod
    def set_summary(obj_type, **kwargs):
        site = os.environ.get('-s', 'default')
        summary = Utils.get_summary()

        for key, value in kwargs.items():
            summary[obj_type][key] = value

        summary_json = f'{TMP_DIR}{os.path.sep}{site}.json'

        with open(summary_json, 'w') as summary_file:
            json.dump(summary, summary_file)

    
    @staticmethod
    def print_summary():
        summary = Utils.get_summary()

        print(f'\n>>>>>  RESUMEN  <<<<<<')

        objs = {'code': 'Código Fuente', 'db': 'Base de Datos', 'img': 'Imágenes'}

        for key, value in summary.items():
            if len(value):
                print(f'[ {objs[key]} ]')
                for k, v in value.items():
                    print(f'- {k}: {v}')

                print('') 

        print(f'>>>>>>>>  ---  <<<<<<<<')

        site = os.environ.get('-s', 'default')
        summary_json = f'{TMP_DIR}{os.path.sep}{site}.json'

        if os.path.exists(summary_json):
            os.remove(summary_json)