import os
from tools.notification import Notification
import settings as st

class Validate():
    errors = []
    noti = Notification()

    def check_params_code(self):
        """Valida que la configuración del sitio a restaurar este completa solo para restaurar código fuente
        Returns:
            [bool]: Verdadero si la configuración esta completa de lo contrario falso
        """
        site = os.environ.get('-s', 'default')
        local_server = st.SITES_RESTORE[site]['LOCAL_SERVER']
        
        try:
            count_errors = 0

            for param in local_server:
                if local_server[param] is None:
                    self.errors.append(f'Asigne un valor al parametro: {param}.')
                    count_errors += 1

            if count_errors > 0:
                self.errors.insert(len(self.errors) - count_errors, '\n----- CONFIG LOCAL SERVER ERRORS -----')
                return False

            return True

        except KeyError:
            self.noti.text_error(f'Error: No hay configuración en el archivo settings.py para el sitio: {site}')
    
    def check_params_db(self):
        """Valida que la configuración del sitio a restaurar este completa solo para restaurar db fuente

        Returns:
            [bool]: Verdadero si la configuración esta completa de lo contrario falso
        """
        site = os.environ.get('-s', 'default')

        try:
            local_db = st.SITES_RESTORE[site]['LOCAL_DB']
            count_errors = 0

            for param in local_db:
                if local_db[param] is None:
                    self.errors.append(f'Asigne un valor al parametro: {param}.')
                    count_errors += 1

            if count_errors > 0:
                self.errors.insert(len(self.errors) - count_errors, '\n----- CONFIG LOCAL DB ERRORS -----')
                return False

            return True
        except KeyError:
            self.noti.text_error(f'Error: No hay configuración en el archivo settings.py para el sitio: {site}')

    def check_params_remote_server(self):
        """Valida que la configuración del sitio a restaurar este completa solo para restaurar db fuente

        Returns:
            [bool]: Verdadero si la configuración esta completa de lo contrario falso
        """
        site = os.environ.get('-s', 'default')

        try:
            remote_server = st.SITES_RESTORE[site]['REMOTE_SERVER']
            count_errors = 0

            for param in remote_server:
                if remote_server[param] is None:
                    self.errors.append(f'Asigne un valor al parametro: {param}.')
                    count_errors += 1
                
                if count_errors > 0:
                    self.errors.insert(len(self.errors) - count_errors, '\n----- CONFIG REMOTE SERVER ERRORS -----')
                    return False

                return True
        except KeyError:
            self.noti.text_error(f'Error: No hay configuración en el archivo settings.py para el sitio: {site}')
        
    def all(self):
        """Validad configuración completa para restaurar código fuente y db

        Returns:
            [bool]: Verdadero si la configuración esta completa de lo contrario falso
        """
        self.check_params_db()
        self.check_params_code()
        
        if not os.environ.get('-src'):
            self.check_params_remote_server()
        
        if len(self.errors) > 0:
            self.noti.text_error(self.errors)
            return False
        
        return True