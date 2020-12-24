import os
from settings import SITES_RESTORE, TMP_DIR, SEP
from tools.cmd import Cmd
from tools.db_actions import DbActions
from tools.notification import Notification
from tools.ssh import Ssh
from tools.tar_file import TarFile

class Database():
    
    SITE = os.environ.get('-s', 'default')
    RS_CONFIG = SITES_RESTORE[SITE]['REMOTE_SERVER']

    def _get_path_sql_file_backup(self):
        """Obtiene la ruta del archivo sql dentro del backup

        Returns:
            str: Ruta del archivo sql del backup
        """
        cmd = Cmd()
        command = [f'find {TMP_DIR}{SEP}db -type f -name "*.sql"']

        result = cmd.execute(command).split('\n')

        if len(result) > 1:
            return result[0]
        else:
            return ''

    def restore(self):
        """Restaura la base de datos a partir de un backup
        """
        cmd = Cmd()
        noti = Notification()
        dba = DbActions()
        tar_file = TarFile()
        
        database = SITES_RESTORE[self.SITE]['LOCAL_DB']['DATABASE']
        user = SITES_RESTORE[self.SITE]['LOCAL_DB']['USER']
        password = SITES_RESTORE[self.SITE]['LOCAL_DB']['PASSWORD']

        if os.environ.get('-src'):
            local_path_tar_db = eval(os.environ.get('-src'))['db']
            tar_file.descompress(local_path_tar_db, 'db')
        else:
            ssh = Ssh()
            tar_bk = ssh.scp_file_download('db')
            tar_file.descompress(tar_bk, 'db')

        sql_file = self._get_path_sql_file_backup()
        
        if dba.isset(database):
            dba.delete(database)
        
        dba.create(database)

        print(f'Restaurando base de datos: {database}')

        try:
            cmd.execute([f"mysql -u {user} -p{password} {database} < {sql_file}"])

            dba.update_shop_url()
            dba.update_configuration()
            dba.disabled_modules()
            dba.set_mode_test_module()

            cmd.execute([f"rm -rf {TMP_DIR}{SEP}db"])
            noti.text_success(f'Base de datos {database} restaurada.')
        except Exception as e:
            noti.text_error(f'Error restaurando la base de datos {database}: {e}')
        