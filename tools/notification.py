from terminal_text_color import TextColor, AlertTextColor

class Notification():

    def print_message(self, type, message):
        """Imprime en la terminal un mensage 

        Args:
            type (str): Tipo de mensaje a mostrar ej: success, error, info, etc
            message (str): Contenido del mensaje a mostrar
        """
        tc = TextColor()
        set_color =  getattr(tc, type)
        
        if isinstance(message, list):
            if len(message) > 0:
                for msg in message:
                    print(set_color(msg))
        else:
            print(set_color(message))
        
        if type == 'default_white_red':
            exit()
    
    def print_alert(self, type, message, title):
        """Imprime en la terminal un mensage tipo alert 

        Args:
            type (str): Tipo de mensaje a mostrar ej: success, error, info, etc
            message (str): Contenido del mensaje a mostrar
        """
        atc = AlertTextColor()
        set_color =  getattr(atc, type)

        if title:
            print(set_color(message, title=title))
        else:
            print(set_color(message))
        
        if type == 'error':
            exit()

    def text_error(self, message):
        """Genera un mensaje de error a mostrar en la terminal

        Args:
            message (str): Contenido del mensaje a mostrar
        """
        self.print_message('default_white_red', message)
    
    def text_success(self, message):
        """Genera un mensaje de éxito a mostrar en la terminal

        Args:
            message (str): Contenido del mensaje a mostrar
        """
        self.print_message('default_white_green', message)

    def alert_success(self, message, title=None):
        """Genera una alert de éxito en la terminal

        Args:
            message (str): Contenido de la alerta a mostrar
        """
        self.print_alert('success', message, title)