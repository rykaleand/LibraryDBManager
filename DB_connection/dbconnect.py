import configparser
from psycopg2.extras import wait_select
import psycopg2
import psycopg2.extensions

global global_config
global_config = None

def read_config():
    config = configparser.ConfigParser()
    config.read('DB_connection/config.ini')
    return config
def connect_to_Database():
    global global_config

    # Первичное чтение конфигурации, если она еще не была прочитана
    if global_config is None:
        global_config = read_config()

    # Получение значений из глобального объекта конфигурации
    db_host = global_config.get('Database', 'host')
    db_port = global_config.get('Database', 'port')
    db_name = global_config.get('Database', 'database')
    db_user = global_config.get('Database', 'username')
    db_password = global_config.get('Database', 'password')

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password)
        return conn
    except Exception as e:
        print(f"Error: Database is not connected: {str(e)}")
        exit(1)
