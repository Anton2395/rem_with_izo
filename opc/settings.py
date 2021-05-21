import psycopg2
import sys
import time
# import os

DB = {
    'dbName': 'db1',
    'host': '10.0.0.2',
    'port': 15432,
    'user': 'mvlab',
    'pass': 'z1x2c3',

    # ToDo: получение credantional из .env
}
# DB = {
#     'dbName': os.getenv('DB_NAME'),
#     'host': os.getenv('DB_HOST'),
#     'port': os.getenv('DB_PORT'),
#     'user': os.getenv('DB_USER'),
#     'pass': os.getenv('DB_PASSWORD'),
#
# }


# функция создания подключения к БД
def createConnection():
    try:
        return psycopg2.connect(dbname=DB['dbName'], user=DB['user'],
                                password=DB['pass'], host=DB['host'])
    except psycopg2.OperationalError as e:
        #ToDo: добавить проверку на соответствующие ошибки метода *.connect

        sys.exit( time.ctime(), f'Unable to connect!\n{e}')

