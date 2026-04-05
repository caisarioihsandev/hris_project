from app.database import get_db

class User:

    @staticmethod
    def find_by_username(username):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            return cursor.fetchone()

    @staticmethod
    def create(username, password, role):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
        db.commit()