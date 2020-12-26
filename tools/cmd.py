import subprocess
from tools.notification import Notification

class Cmd():
    noti = Notification()

    def execute(self, command, mode='r'):
        """Ejecuta un comando de consola.

        Args:
            command (list): Comando a ser ejecutado ej: ['ls', '-la'].
            mode (str, optional): Modo r=lectura w=escritura.

        Returns:
            str: Resulatado de la ejecución del comando.
        """
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out, err = proc.communicate()

        if err:
            self.noti.text_error(f'Command error: {err}')

        return out.decode('utf-8')