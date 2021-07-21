import os
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