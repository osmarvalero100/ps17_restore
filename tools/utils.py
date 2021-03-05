from .cmd import Cmd

class Utils():
    """
    Métodos utiles de uso general
    """
    
    def get_file_size(self, path_bk):
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
        