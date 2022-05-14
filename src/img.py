import os
from settings import SITES_RESTORE, SEP
from tools.cmd import Cmd
from tools.notification import Notification
from tools.ssh import Ssh
from tools.tar_file import TarFile
from tools.utils import Utils

class Img():

    def __init__(self):
        self.SITE = os.environ.get('-s', 'default')
        self.RS_CONFIG = SITES_RESTORE[self.SITE]['REMOTE_SERVER']
        self.PATH_HTDOCS_DIR = f"{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['ROOT_SITE']}"

    def get_path_folder_img_backup(self):
        """Obtiene la ruta de la carpeta de las imágenes del proyecto en el backup

        Returns:
            str: Ruta de carpeta de imágenes del backup
        """
        cmd = Cmd()
        object_path = Utils.get_tmp_path_site_by_object('img')
        command = [f'find {object_path} -type d -name admin']
        result = cmd.execute(command)

        return result.replace(f'{SEP}admin\n', '')

    def _set_permissions(self):
        """ Asigna permisos a la carpeta del proyecto """
        noti = Notification()
        try:
            if 'PERMISSIONS' in SITES_RESTORE[self.SITE]['LOCAL_SERVER']:
                permissions = SITES_RESTORE[self.SITE]['LOCAL_SERVER']['PERMISSIONS']
                if 'chown' in permissions and len(str(permissions['chown'])):
                    os.system(f'chown -R {permissions["chown"]} {self.PATH_HTDOCS_DIR}{SEP}img')
                if 'chmod' in permissions and len(str(permissions['chmod'])):
                    os.system(f'chmod -R {permissions["chmod"]} {self.PATH_HTDOCS_DIR}{SEP}img')
        except Exception as e:
            noti.text_error(f'Error asignando permisos a htdocs y logs: {e}.')

    def restore(self):
        tar_file = TarFile()

        if os.environ.get('-src'):
            local_path_tar_code = eval(os.environ.get('-src'))['img']
            tar_file.descompress(local_path_tar_code, 'img')
        else:
            ssh = Ssh()
            tar_bk = ssh.scp_file_download('img')
            tar_file.descompress(tar_bk, 'img') 

        path_img_backup = self.get_path_folder_img_backup()
        path_img = f'{self.PATH_HTDOCS_DIR}{SEP}img'

        cmd = Cmd()
        if os.path.isdir(path_img):
            cmd.execute([f'rm -rf {path_img}'])

        command = [f'mv {path_img_backup} {self.PATH_HTDOCS_DIR}']
        cmd.execute(command)
        self._set_permissions()

        object_path = Utils.get_tmp_path_site_by_object('img')
        cmd.execute([f"rm -rf {object_path}"])

        noti = Notification()
        noti.text_success(f'Imágenes restauradas.')