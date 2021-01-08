import os
import time
import shutil
import paramiko
from settings import SEP, SITES_RESTORE, TMP_DIR, USER_OS
from tools.notification import Notification

class Ssh():
    ssh_client = None
    noti = None
    progress = 0
    

    def __init__(self):
        self.noti = Notification()
        self.SITE = os.environ.get('-s', 'default')
        self.RS_CONFIG = SITES_RESTORE[self.SITE]['REMOTE_SERVER']
        
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.RS_CONFIG['HOST'], username=os.environ['RS_USER'], password=os.environ['RS_PASS'])
        except paramiko.SSHException as e:
            self.noti.text_error(f"Usuario o contraseña incorrecta para server {self.RS_CONFIG['HOST']}: {e}")

    def get_file_name_remote_backup(self, dir, obj_type):
        """Obtiene el nombre del archivo que contiene el backup de code, db ó img

        Args:
            dir (str): Ruta del directorio que contine el archivo a obtener
            obj_type (str): Tipo de objeto a restaurar puueder ser code, db o img

        Returns:
            [str]: Nombre del último archivo creado en el directorio
        """
        if os.environ.get('-szdb') and obj_type=='db':
            # obtiene el archivo de mayor tamaño no mayor a 1 dia de antiguedad
            cmd = f'find  {dir} -type f -mtime -1| xargs ls -ltr | sort -nk5 | tail -1'
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            time.sleep(1)
            tmp_res = stdout.read().decode()
            result = tmp_res.split(f'{self.RS_CONFIG["FOLDER_DB"]}{SEP}')[1]

        elif os.environ.get('-rsrc'):
        
            return eval(os.environ.get('-rsrc'))[obj_type]
        else:
            # Obtiene el último archivo creado
            cmd = f'cd {dir} && ls -Art | tail -n 1'
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            time.sleep(1)
            result = stdout.read().decode()

        if not result:
            raise  self.noti.text_error(f'El directorio remoto: {dir}. No existe o está vacio.')

        name_file = result.split('\n')[0]
        
        return name_file

    def print_progress(self, transferred, toBeTransferred):
        """Muestra en consola el porcentaje de descarga del backup

        Args:
            transferred (int): Total transferido
            toBeTransferred (int): Total a transferir
        """
        percentage = int(((transferred / toBeTransferred) * 100))

        if percentage % 5 == 0 and percentage > self.progress:
            self.progress = percentage
            print(f'Descarga: {percentage}% de 100%')
            if percentage == 100:
                self.noti.text_success('Descarga finalizada.')

    def scp_file_download(self, obj_type):
        """Descarga el último backup de código fuente, db o img

        Args:
            obj_type (str): Tipo de objeto a restaurar puueder ser code, db o img

        Returns:
            [str]: Ruta del archivo descargado
        """
        rs_dir = self.RS_CONFIG[f'FOLDER_{obj_type.upper()}']
        tar_remote_file = self.get_file_name_remote_backup(rs_dir, obj_type)

        if tar_remote_file[-7:] == '.tar.gz':
            object_path = f'{TMP_DIR}{SEP}{obj_type}'

            if os.path.isdir(object_path):
                shutil.rmtree(object_path)

            os.makedirs(object_path, exist_ok = True)
            try:
                sftp_client =  self.ssh_client.open_sftp()
                remote_file = f'{rs_dir}{SEP}{tar_remote_file}'
                local_file = f'{TMP_DIR}{SEP}{obj_type}{SEP}{tar_remote_file}'

                # Descarga backup del servidor y se guarda en directorio local tmp
                print(f'Inicia la descarga del backup {obj_type}')
                print(f'( {tar_remote_file} )')
                
                sftp_client.get(
                    remote_file,
                    local_file,
                    callback=self.print_progress
                )
                self.progress = 0
                self.ssh_client.close()
                os.system(f'chown -R {USER_OS} {TMP_DIR}')
                os.system(f'chmod -R 775 {TMP_DIR}')

                return local_file
            except Exception as e:
                self.noti.text_error(f'Error descargando backup {obj_type}: {e}')
        else:
            self.noti.text_error(f'El archivo backup {tar_remote_file} debe tener la extensión: .tar.gz')
        