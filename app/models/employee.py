from app.database import get_db

class Employee:
    
    @staticmethod # decorator: "Employee.get_all()"
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM karyawan")
            return cursor.fetchall()
    
    @staticmethod
    def get_karyawan(id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    gaji_pokok,
                    tunj_jabatan,
                    tunj_makan,
                    tunj_transport,
                    premi_kehadiran
                FROM karyawan
                WHERE id=%s
            """, (id,))
            
        return cursor.fetchone()

    @staticmethod # decorator: "Employee.create(data)"
    def create(data):
        db = get_db()
        with db.cursor() as cursor: 
            sql = """
            INSERT INTO karyawan (nama, jabatan, kode, gaji_pokok, tunj_jabatan, tunj_makan, tunj_transport, premi_kehadiran)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (data['nama'], data['jabatan'], data['kode'], data['gaji_pokok'], data['tunj_jabatan'], data['tunj_makan'], data['tunj_transport'], data['premi_kehadiran']))
        db.commit()

    @staticmethod
    def update(data):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE karyawan
                SET nama=%s, jabatan=%s, kode=%s, gaji_pokok=%s, tunj_jabatan=%s, tunj_makan=%s, tunj_transport=%s, premi_kehadiran=%s
                WHERE id=%s
            """, (data['nama'], data['jabatan'], data['kode'], data['gaji_pokok'], data['tunj_jabatan'], data['tunj_makan'], data['tunj_transport'], data['premi_kehadiran'], data['id']))
        db.commit()


    @staticmethod
    def delete(id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM karyawan WHERE id=%s", (id,))
        db.commit()