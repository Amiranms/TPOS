from flask import Flask, jsonify, make_response
import pymysql
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)




def get_db_connection():
    logger.info("Соединение с базой установлено.")
    return pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
    )


@app.route('/')
def get_all_data():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/health')
def health_check():
    return jsonify({"status": "OK"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
    logger.info("Загрузка .env файла")
    load_dotenv('./db_env.env')
    app.run(host='0.0.0.0', port=8000)