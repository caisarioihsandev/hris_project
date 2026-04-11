from app.database import get_db
from datetime import datetime, time

class Attendance:

    @staticmethod
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT a.*, e.nama 
                FROM absensi a
                JOIN karyawan e ON e.id = a.id_karyawan
                ORDER BY tanggal DESC
            """)
            return cursor.fetchall()
        
    @staticmethod
    def create(data):
        db = get_db()

        # logic stat_on_time
        stat_on_time = None

        if data['stat_kehadiran'] == 'MASUK' and data['check_in']:
            jam_masuk = time(8, 0)
            check_in = datetime.strptime(data['check_in'], "%H:%M").time()

            stat_on_time = 1 if check_in <= jam_masuk else 0

        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO absensi 
                (id_karyawan, tanggal, check_in, check_out, stat_kehadiran, stat_on_time, keterangan)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data['id_karyawan'],
                data['tanggal'],
                data['check_in'] or None,
                data['check_out'] or None,
                data['stat_kehadiran'],
                stat_on_time,
                data['keterangan']
            ))
        db.commit()
    
    @staticmethod
    def update(data):
        db = get_db()

        # logic stat_on_time
        stat_on_time = None

        if data['stat_kehadiran'] == 'MASUK' and data['check_in']:
            jam_masuk = time(8, 0)
            check_in = datetime.strptime(data['check_in'], "%H:%M").time()

            stat_on_time = 1 if check_in <= jam_masuk else 0

        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE absensi
                SET id_karyawan=%s, tanggal=%s, check_in=%s, check_out=%s, stat_kehadiran=%s, stat_on_time=%s, keterangan=%s
                WHERE id=%s
            """, (data['id_karyawan'], data['tanggal'], data['check_in'], data['check_out'], data['stat_kehadiran'], stat_on_time, data['keterangan'], data['id']))
        db.commit()


    @staticmethod
    def delete(id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM absensi WHERE id=%s", (id,))
        db.commit()