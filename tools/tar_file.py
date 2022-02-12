import tarfile
from tools.notification import Notification
from .utils import Utils
from settings import SEP, TMP_DIR


class TarFile():
    """
    Comprir o descomprimir archivos
    """

    def descompress(self, file, type_obj):
        """Descomprime el archvo backup .tar.gz

        Args:
            file (str): ruta del archivo a descomprimir
            type_obj (str): tipo de objeto: code, db ó img
        """
        noti = Notification()
        
        size_bk = Utils.get_file_size(file)
        object_path = Utils.get_tmp_path_site_by_object(type_obj)

        print(f'\nDescomprimiendo backup {type_obj} ( {size_bk} )')

        try:
            f = tarfile.open(file, 'r:gz')
            with f as t:
                t.extractall(f'{object_path}')
            f.close()
            noti.text_success('Descompresión finalizada.')
        except Exception as e:
            noti.text_error(f'No fue posible descomprimir backup {type_obj}: {e}')