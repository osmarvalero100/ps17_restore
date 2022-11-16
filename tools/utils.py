import os
import json
import time
from datetime import datetime, timedelta
from settings import TMP_DIR, SEP
from .cmd import Cmd

class Utils():
    """
    Métodos utiles de uso general
    """

    def update_restore_progress(obj_type, message):
        """Imprime en terminal el avance de la restuación de cada backup
        """
        if obj_type == 'db':
            print(f"~ \033[1mDB\033[0m[ {message} ]")
        if obj_type == 'code':
            print(f"~ \033[1mCode\033[0m[ {message} ]")
        if obj_type == 'img':
            print(f"~ \033[1mImg\033[0m[ {message} ] ")

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

        print(f'\n  Resumen Backup')

        objs = {'code': 'Código Fuente', 'db': 'Base de Datos', 'img': 'Imágenes'}

        for key, value in summary.items():
            if len(value):
                print(f'[ {objs[key]} ]')
                for k, v in value.items():
                    print(f'- {k}: {v}')
                print('\t---')

        site = os.environ.get('-s', 'default')
        summary_json = f'{TMP_DIR}{os.path.sep}{site}.json'
        total_time_bks = Utils.get_time_restore(float(os.environ.get('start_time_bk')))

        print('[ Total time ]')
        print(f'- time: {total_time_bks}')
        print('\t---')

        if os.path.exists(summary_json):
            os.remove(summary_json)

    @staticmethod
    def get_time_restore(start_time):
        total_time = time.time() - start_time
        sec = timedelta(seconds=total_time)
        d = datetime(1,1,1) + sec
        days = d.day-1 if d.day-1 > 9 else f'0{d.day-1}'
        hours = d.hour if d.hour > 9 else f'0{d.hour}'
        minutes = d.minute if d.minute > 9 else f'0{d.minute}'
        seconds = d.second if d.second > 9 else f'0{d.second}'
        time_bk = ''

        if int(days) > 0:
            time_bk = f'{time_bk} {days}d'

        return f'{time_bk} {hours}:{minutes}:{seconds}'.strip()