import pymysql
import os
from dotenv import load_dotenv
import pandas as pd
import logging
import time

# logger initialization
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# queries

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL
);
"""

INSERT_DATA_QUERY = """
INSERT INTO users (name, age) VALUES (%s, %s);
"""

PRINT_DATA_QUERY = """
SELECT * FROM users;
"""

def get_connection():
    return pymysql.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT')),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )

def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            connection = get_connection()
            connection.close()
            return
        except pymysql.MySQLError as e:
            logger.info(f"База данных недоступна, повтор через 5 секунд... ({retries} попыток осталось)")
            print(e)
            retries -= 1
            time.sleep(5)
        except:
            raise Exception("Не удалось подключиться к базе данных.")

def connect_to_db():
    try:
        connection = get_connection()
        logger.info('Соединение установлено.')
        return connection
    except pymysql.MySQLError as e:
        logger.error(f"Ошибка при установке соединения с базой данных: {e}")


def fill_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
        logger.info('База данных создана.')

        user_data_df = pd.read_csv(os.getenv('DATA_PATH'))
        for name, age in user_data_df.iloc:
            cursor.execute(INSERT_DATA_QUERY, (name, int(age)))
        logger.info('Данные загружены.')

        connection.commit()
        logger.info('Транзакция завершена.')

    except pymysql.MySQLError as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")




def print_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(PRINT_DATA_QUERY)
        for row in cursor.fetchall():
            print(row)

    except pymysql.MySQLError as e:
        logger.error(f"Ошибка в процессе вывода данных в stdout: {e}")

    finally:
        connection.close()
        logger.info("Отключение от базы данных.")




if __name__ == '__main__':

    logger.info("Загрузка .env файла")
    load_dotenv('./db_env.env')
    wait_for_db()
    logger.info("БД доступна для подключения.")
    connection = connect_to_db()
    fill_db(connection)
    print_db(connection)












