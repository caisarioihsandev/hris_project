import pymysql

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Kmzwa85wa#',
        database='hris_db',
        cursorclass=pymysql.cursors.DictCursor
    )