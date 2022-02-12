import secrets 
import os
import random
from tools.cmd import Cmd
from tools.ssh import Ssh
from settings import SITES_RESTORE, SEP
from tools.db_actions import DbActions
from tools.notification import Notification
from tools.tar_file import TarFile
from tools.utils import Utils

class Code():
    
    def __init__(self):
        self.SITE = os.environ.get('-s', 'default')
        self.PATH_HTDOCS_DIR = f"{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['ROOT_SITE']}"

    def _get_path_folder_root_backup(self):
        """Obtiene la ruta de la carpeta raíz del proyecto en el backup

        Returns:
            str: Ruta de carpeta raíz del proyecto en el backup
        """
        cmd = Cmd()
        object_path = Utils.get_tmp_path_site_by_object('code')

        for root_dir in ['htdocs', 'html']:
            command = [f'find {object_path} -type d -name {root_dir}']
            result = cmd.execute(command)

            if result:
                return result
                break

        return None

    def __create_file_parameters(self):
        """ Crear el archivo app/config/parmeters.php """
        noti = Notification()

        try:
            if os.path.isdir(self.PATH_HTDOCS_DIR):
                ps_file_param = f'{self.PATH_HTDOCS_DIR}{SEP}app{SEP}config{SEP}parameters.php'

                if os.path.exists(ps_file_param):
                    os.remove(ps_file_param)

                new_cookie_key = f"{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['NEW_COOKIE_KEY']}"

                f = open(ps_file_param, 'a')
                f.write("<?php return array (\r")
                f.write("\t'parameters' =>\r")
                f.write("\tarray (\r")
                f.write("\t\t'database_host' => '{}',\r".format(SITES_RESTORE[self.SITE]['LOCAL_DB']['HOST']))
                f.write("\t\t'database_port' => '{}',\r".format(SITES_RESTORE[self.SITE]['LOCAL_DB']['PORT']))
                f.write("\t\t'database_name' => '{}',\r".format(SITES_RESTORE[self.SITE]['LOCAL_DB']['DATABASE']))
                f.write("\t\t'database_user' => '{}',\r".format(SITES_RESTORE[self.SITE]['LOCAL_DB']['USER']))
                f.write("\t\t'database_password' => '{}',\r".format(SITES_RESTORE[self.SITE]['LOCAL_DB']['PASSWORD']))
                f.write("\t\t'database_prefix' => '{}',\r".format(SITES_RESTORE[self.SITE]['LOCAL_DB']['PS_PREFIX']))
                f.write("\t\t'database_engine' => 'InnoDB',\r")
                f.write("\t\t'mailer_transport' => 'smtp',\r")
                f.write("\t\t'mailer_host' => '127.0.0.1',\r")
                f.write("\t\t'mailer_user' => NULL,\r")
                f.write("\t\t'mailer_password' => NULL,\r")
                f.write(f"\t\t'secret' => '{secrets.token_urlsafe(random.randint(53, 79))}',\r")
                f.write("\t\t'ps_caching' => 'CacheMemcache',\r")
                f.write("\t\t'ps_cache_enable' => false,\r")
                f.write(f"\t\t'ps_creation_date' => '{random.randint(2018, 2020)}-{random.randint(1, 12)}-{random.randint(1, 28)}',\r")
                f.write("\t\t'locale' => 'es-ES',\r")
                f.write(f"\t\t'cookie_key' => '{secrets.token_urlsafe(random.randint(49, 74))}',\r")
                f.write(f"\t\t'cookie_iv' => '{secrets.token_urlsafe(8)}',\r")
                f.write(f"\t\t'new_cookie_key' => '{new_cookie_key}',\r")
                f.write("\t),\r")
                f.write(");")
                f.close()
            else:
                noti.text_error(f'No se encontro el directorio {self.PATH_HTDOCS_DIR}.')
        except Exception as e:
            noti.text_error(f'Error creando archivo parameters.php {e}.')

    
    def _update_file_robots(self):
        """ Actualiza archivo robots """
        noti = Notification()
        robots_file = f'{self.PATH_HTDOCS_DIR}{SEP}robots.txt'

        try:
            if os.path.exists(robots_file):
                os.remove(robots_file)

            f = open(robots_file, 'a')
            f.write("User-agent: *\r")
            f.write("Disallow: /\r")
            f.close()
        except Exception as e:
            noti.text_error(f'Error actualizando archivo robots.txt {e}.')


    def _set_default_prod_img(self):
        """ Crea la imagen por defecto para los productos sin imagen
        """
        dba = DbActions()
        iso_code = dba.get_iso_code()
        folder_img_prods = f"{self.PATH_HTDOCS_DIR}{SEP}img{SEP}p"

        if not os.path.exists(folder_img_prods):
            os.system('mkdir -p folder_img_prods')

        url_img_default = f"{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['DEFAULT_PRODUCT_IMG']}"
        os.system(f"cd {folder_img_prods} && wget -q -cO - {url_img_default} > {iso_code}.jpg")
        

    def _set_permissions(self):
        """ Asigna permisos a la carpeta del proyecto """
        noti = Notification()
        logs_dir = f"{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['LOGS_DIR']}"
        chown = f"{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['PERMISSIONS']['chown']}"
        chmod = f"{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['PERMISSIONS']['chmod']}"
        
        try:
            os.makedirs(logs_dir, exist_ok=True)
            os.system(f'chown -R {chown} {self.PATH_HTDOCS_DIR} {logs_dir}')
            os.system(f'chmod -R {chmod} {self.PATH_HTDOCS_DIR} {logs_dir}')
        except Exception as e:
            noti.text_error(f'Error asignando permisos a htdocs y logs: {e}.')
        

    def restore(self):
        """Restaura el codígo fuente del sitio Prestashop a partir de un backup
        """
        cmd = Cmd()
        noti = Notification()
        tar_file = TarFile()

        if os.environ.get('-src'):
            local_path_tar_code = eval(os.environ.get('-src'))['code']
            tar_file.descompress(local_path_tar_code, 'code')
        else:
            ssh = Ssh()
            tar_bk = ssh.scp_file_download('code')
            tar_file.descompress(tar_bk, 'code')

        print('Restaurando code')
        # Elimina el código fuente antiguo
        rm_command = [f'rm -rf {self.PATH_HTDOCS_DIR}*']
        cmd.execute(rm_command)

        # Renueva el código fuente
        os.makedirs(self.PATH_HTDOCS_DIR, exist_ok=True)
        path_htdocs_backup = self._get_path_folder_root_backup().split('\n')[0]
        mv_command = [f'cp -r {path_htdocs_backup}{SEP}. {self.PATH_HTDOCS_DIR}']
        cmd.execute(mv_command)

        self.__create_file_parameters()
        self._update_file_robots()

        if not os.environ.get('-full'):
            self._set_default_prod_img()

        self._set_permissions()

        url_site = f"http://{SITES_RESTORE[self.SITE]['LOCAL_SERVER']['SHOP_URL']}"
        object_path = Utils.get_tmp_path_site_by_object('code')
        
        cmd.execute([f"rm -rf {object_path}"])
        #cmd.execute([f"x-www-browser {url_site}"])
        
        noti.text_success(f'Código fuente restaurado.')
        
        site = os.environ.get('-s', 'default')
        noti.alert_success(f'Tu sitio está listo. Visítalo ahora: {url_site}')


       
