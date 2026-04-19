from app.database import get_db

class User:

    @staticmethod
    def find_by_username(username):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            return cursor.fetchone()
        
    @staticmethod
    def get_all():
        db=get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

    @staticmethod
    def create(data):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (data['username'], data['password'], data['role'])
            )
        db.commit()

    @staticmethod
    def update(data):
        db = get_db()
        db.execute("""
            UPDATE users 
            SET username=%s, password=%s, role=%s
            WHERE id=%s
        """, (data['username'], data['password'], data['role'], data['id']))

    @staticmethod
    def delete(id):
        db = get_db()
        db.execute("DELETE FROM users WHERE id=%s", (id,))