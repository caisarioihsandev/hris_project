import os
import pymysql
from config import Config

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", Config.MYSQL_HOST),
        user=os.getenv("DB_USER", Config.MYSQL_USER),
        password=os.getenv("DB_PASSWORD", Config.MYSQL_PASSWORD),
        database=os.getenv("DB_NAME", Config.MYSQL_DB),
        port=int(os.getenv("DB_PORT", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )