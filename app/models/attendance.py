from app.database import get_db
from datetime import datetime

class Attendance:

    @staticmethod
    def check_in(id_karyawan):
        db = get_db()
        now = datetime.now()

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO attendance (employee_id, tanggal, check_in, status)
                VALUES (%s, %s, %s, %s)
            """, (
                id_karyawan,
                now.date(),
                now.time(),
                "Hadir"
            ))
        db.commit()


    @staticmethod
    def check_out(id_karyawan):
        db = get_db()
        now = datetime.now()

        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE attendance
                SET check_out=%s
                WHERE employee_id=%s AND tanggal=%s
            """, (
                now.time(),
                id_karyawan,
                now.date()
            ))
        db.commit()


    @staticmethod
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT a.*, e.nama 
                FROM attendance a
                JOIN employees e ON e.id = a.employee_id
                ORDER BY tanggal DESC
            """)
            return cursor.fetchall()