# -*- coding: utf-8 -*-
import os
import pymysql
from settings import SITES_RESTORE
from tools.notification import Notification

class DbActions:

    SITE = os.environ.get('-s', 'default')
    DB_CONFIG = SITES_RESTORE[SITE]['LOCAL_DB']
    db_cursor = None
    noti = None

    def __init__(self):
        self.noti = Notification()

    def __connect(self, db = DB_CONFIG['DATABASE']):
        """Conexión a la base de datos.

        Args:
            db (str), optional): Nombre de la base de datos a conectar.
        """
        try:
            if db:
                connection = pymysql.connect(host=self.DB_CONFIG['HOST'], user=self.DB_CONFIG['USER'], password=self.DB_CONFIG['PASSWORD'],
                                            database=db, charset=self.DB_CONFIG['CHARSET'], cursorclass=pymysql.cursors.DictCursor, autocommit=True)
            else:
                connection = pymysql.connect(host=self.DB_CONFIG['HOST'], user=self.DB_CONFIG['USER'], password=self.DB_CONFIG['PASSWORD'],
                                              charset=self.DB_CONFIG['CHARSET'], cursorclass=pymysql.cursors.DictCursor, autocommit=True)
                
            self.db_cursor = connection.cursor()
        except Exception as e:
            self.noti.text_error(f'Error en conexión a db: {e}')
    
    def isset(self, name):
        """Valida si una base de datos ya existe

        Args:
            name (str): Nombre de la base de datos

        Returns:
            bool: Verdadero si la base de datos existe de lo contario falso
        """
        self.__connect(None)
        self.db_cursor.execute('SHOW DATABASES')
        databases = self.db_cursor.fetchall()
        self.db_cursor.close()

        for database in databases:
            if database['Database'] == name:
                return True

        return False
    
    def create(self, name):
        """Crea una nueva base de datos

        Args:
            name (str): Nombre de la base de datos
        """
        print(f'Creando base de datos: {name}')

        try:
            self.__connect(None)
            self.db_cursor.execute(f'CREATE DATABASE {name}')
            self.db_cursor.execute(f"ALTER DATABASE {name} CHARACTER SET {self.DB_CONFIG['CHARSET']} COLLATE {self.DB_CONFIG['COLLATION']}")
            self.db_cursor.close()
            self.noti.text_success(f'Base de datos {name} creada.')
        except Exception as e:
            self.noti.text_error(f'Error al crear la base de datos {name}: {e}')

    def delete(self, name):
        """Elimina una base de datos

        Args:
            name (str): Nombre de la base de datos a eliminar
        """

        if self.isset(name):
            print(f'Eliminando base de datos: {name}')

            try:
                self.__connect(None)
                self.db_cursor.execute(f'DROP DATABASE {name}')
                self.db_cursor.close()
                self.noti.text_success(f'Base de datos {name} eliminada.')
            except Exception as e:
                self.noti.text_error(f'Error al eliminar la base de datos {name}: {e}')

    def update_shop_url(self):
        """Actualiza la URL del sitio """
        local_domain = SITES_RESTORE[self.SITE]['LOCAL_SERVER']['SHOP_URL']
        id_shop = SITES_RESTORE[self.SITE]['LOCAL_SERVER']['ID_SHOP']
        
        try:
            self.__connect()
            sql = f"UPDATE {self.DB_CONFIG['PS_PREFIX']}shop_url SET domain = '{local_domain}', domain_ssl = '{local_domain}' WHERE id_shop = {id_shop}"
            self.db_cursor.execute(sql)
            self.db_cursor.close()
            print(F'- Shop Domain cambiado a: {local_domain}')

        except (pymysql.OperationalError, pymysql.InternalError, pymysql.ProgrammingError) as e:
            self.noti.text_error(f"Error al actualizar la tabla {self.DB_CONFIG['PS_PREFIX']}shop_url: {e}")

    def update_configuration(self):
        """ Actualiza el dominio del sitio y desactiva el SSL del sitio """
        local_domain = SITES_RESTORE[self.SITE]['LOCAL_SERVER']['SHOP_URL']

        try:
            self.__connect()
            sql = f"UPDATE {self.DB_CONFIG['PS_PREFIX']}configuration SET value = '{local_domain}' WHERE name IN('PS_SHOP_DOMAIN','PS_SHOP_DOMAIN_SSL','PS_MAIL_DOMAIN')"
            self.db_cursor.execute(sql)

            sql = f"UPDATE {self.DB_CONFIG['PS_PREFIX']}configuration SET value = '0' WHERE name IN('PS_SSL_ENABLED','PS_SSL_ENABLED_EVERYWHERE')"
            self.db_cursor.execute(sql)
            self.db_cursor.close()
        except (pymysql.OperationalError, pymysql.InternalError, pymysql.ProgrammingError) as e:
            self.noti.text_error(f"Error al actualizar la tabla {self.DB_CONFIG['PS_PREFIX']}configuration: {e}")
        

    def disabled_modules(self):
        """Desactivar módulos para la tienda """
        if len(SITES_RESTORE[self.SITE]['MODULES']['disable']) > 0:
            name_modules = ''
            for module in SITES_RESTORE[self.SITE]['MODULES']['disable']:
                name_modules += "'{}',".format(module)
                
            try:
                self.__connect()
                sql = f"SELECT id_module, name FROM {self.DB_CONFIG['PS_PREFIX']}module WHERE name IN ({name_modules[:-1]})"
                self.db_cursor.execute(sql)
                ids_module = self.db_cursor.fetchall()

                for item in ids_module:
                    sql = f"DELETE FROM {self.DB_CONFIG['PS_PREFIX']}module_shop WHERE id_module = {item['id_module']}"
                    self.db_cursor.execute(sql)
                    print(f'- Módulo:disahabilitado: {item["name"]}')

                self.db_cursor.close()
            except (pymysql.OperationalError, pymysql.InternalError, pymysql.ProgrammingError) as e:
                self.noti.text_error(f'Error desactivando módulos: {e}')
            

    def set_mode_test_module(self):
        """Asigna el modo Sandbox a módulos por base de datos """
        try:
            self.__connect()

            if len(SITES_RESTORE[self.SITE]['MODULES']['sandbox']['vars']) > 0:
                for var in SITES_RESTORE[self.SITE]['MODULES']['sandbox']['vars']:
                    sql = f"UPDATE {self.DB_CONFIG['PS_PREFIX']}configuration SET value = '0' WHERE name = '{var}'"
                    self.db_cursor.execute(sql)
                    print(f'- Variable de conf cambiada a modo sanbox: {var}')

                self.db_cursor.close()
        except (pymysql.OperationalError, pymysql.InternalError, pymysql.ProgrammingError) as e:
            self.noti.text_error(f'Error asignando modo sanbox a módulos: {e}')
        

    def get_iso_code(self):
        """ Obtiene el iso_code de la tienda
        """
        id_shop = SITES_RESTORE[self.SITE]['LOCAL_SERVER']['ID_SHOP']
        self.__connect()
        sql = f"SELECT pl.iso_code FROM ps_lang_shop pls JOIN ps_lang pl ON pls.id_lang = pl.id_lang WHERE pls.id_shop = {id_shop} LIMIT 1"
        
        if self.db_cursor.execute(sql):
            return self.db_cursor.fetchone()['iso_code']
        else:
            return 'es'
        
        
        