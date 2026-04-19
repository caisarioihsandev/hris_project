from app.database import get_db

class Payroll:

    @staticmethod # decorator: "Payroll.get_all()"
    def get_all():
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT p.*, e.nama, e.premi_kehadiran FROM payroll p JOIN karyawan e ON e.id = p.id_karyawan")
            return cursor.fetchall()
        
    @staticmethod
    def get_one(id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, e.nama, e.kode 
                FROM payroll p
                JOIN karyawan e ON e.id = p.id_karyawan
                WHERE p.id=%s
            """, (id,))
            return cursor.fetchone()

    @staticmethod
    def get_absensi_summary(id_karyawan, periode):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN stat_kehadiran='ALPA' THEN 1 ELSE 0 END) as total_alpha,
                    SUM(CASE WHEN stat_on_time=0 THEN 1 ELSE 0 END) as total_telat
                FROM absensi
                WHERE id_karyawan=%s
                AND DATE_FORMAT(tanggal, '%Y-%m')=%s
            """, (id_karyawan, periode))

            return cursor.fetchone()

    @staticmethod
    def hitung(data):
        gaji = float(data['gaji_pokok'])
        tunj_jabatan = float(data.get('tunj_jabatan', 0))
        tunj_makan = float(data.get('tunj_makan', 0))
        tunj_transport = float(data.get('tunj_transport', 0))
        premi_kehadiran = float(data.get('premi_kehadiran', 0))
        hari_kerja = int(data.get('tot_hari_kerja', 0))

        upah_tetap = gaji + tunj_jabatan

        # 🔥 ABSENSI
        # summary = Payroll.get_absensi_summary(data['id_karyawan'], data['periode'])
        # alpha = summary['total_alpha'] or 0
        # telat = summary['total_telat'] or 0

        # Kehadiran dan potongan absensi
        tot_premi_kehadiran = premi_kehadiran * hari_kerja
        pot_alpha = premi_kehadiran * 0
        pot_telat = premi_kehadiran * 0.5 * 0
        pot_absen = pot_alpha + pot_telat

        upah_penuh = upah_tetap + tunj_makan + tunj_transport + tot_premi_kehadiran

        # BPJS yang ditanggung Perusahaan
        bpjs_kes_tg_perusahaan = upah_tetap * 0.04 #(4%)
        bpjs_tk_tg_perusahaan = upah_tetap * (0.0089 + 0.003 + 0.037 + 0.02) # JKK (0.89%) + JKM (0.30%) + JHT(3.70%) + JP (2.00%)

        # Potangan BPJS
        pot_bpjs_kes = 0.01 * upah_tetap # (1%)
        pot_bpjs_tk = 0.03 * upah_tetap # JHT 2% + JP 1%

        # Pajak
        biaya_jabatan = min(0.05 * upah_tetap, 500000)
        neto = upah_penuh - biaya_jabatan
        neto_tahun = neto * 12
        pkp = max(0, neto_tahun - 54000000)
        pph21 = (0.05 * pkp) / 12

        total_potongan = pot_bpjs_kes + pot_bpjs_tk + pph21 + pot_absen
        gaji_bersih = upah_penuh - total_potongan

        return {
            'tot_hari_kerja': hari_kerja,
            'tot_premi_kehadiran': tot_premi_kehadiran,
            'upah_tetap': upah_tetap,
            'upah_penuh': upah_penuh,
            'bpjs_kes_tg_perusahaan': bpjs_kes_tg_perusahaan,
            'bpjs_tk_tg_perusahaan': bpjs_tk_tg_perusahaan,
            'pot_bpjs_kes': pot_bpjs_kes,
            'pot_bpjs_tk': pot_bpjs_tk,            
            'pph21': pph21,
            'pot_alpha': pot_alpha,
            'pot_telat': pot_telat,
            'pot_absen': pot_absen,
            'total_potongan': total_potongan,
            'gaji_bersih': gaji_bersih
        }

    @staticmethod
    def create(data):
        hasil = Payroll.hitung(data)

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO payroll 
                (id_karyawan, periode, tot_hari_kerja, gaji_pokok, tunj_jabatan,
                 upah_tetap, tunj_makan, tunj_transport, tot_premi_kehadiran,                 
                 bpjs_kes_tg_perusahaan, bpjs_tk_tg_perusahaan, upah_penuh,
                 pot_alpha, pot_telat, pot_absen, pot_pph21, pot_bpjs_kes,
                 pot_bpjs_tk, total_potongan, gaji_bersih, keterangan)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                data['id_karyawan'],
                data['periode'],
                data['tot_hari_kerja'],
                data['gaji_pokok'],
                data.get('tunj_jabatan', 0),
                hasil['upah_tetap'],
                data.get('tunj_makan', 0),
                data.get('tunj_transport', 0),
                hasil['tot_premi_kehadiran'],
                hasil['bpjs_kes_tg_perusahaan'],
                hasil['bpjs_tk_tg_perusahaan'],
                hasil['upah_penuh'],
                hasil['pot_alpha'],
                hasil['pot_telat'],
                hasil['pot_absen'],
                hasil['pph21'],
                hasil['pot_bpjs_kes'],
                hasil['pot_bpjs_tk'],
                hasil['total_potongan'],
                hasil['gaji_bersih'],
                data['keterangan']
            ))
        db.commit()

    @staticmethod
    def update(data):
        hasil = Payroll.hitung(data)

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE payroll SET
                id_karyawan=%s,
                periode=%s,
                gaji_pokok=%s,
                tunj_jabatan=%s,
                upah_tetap=%s,
                tunj_makan=%s,
                tunj_transport=%s,
                tot_premi_kehadiran=%s,
                bpjs_kes_tg_perusahaan=%s,
                bpjs_tk_tg_perusahaan=%s,
                upah_penuh=%s,
                pot_alpha=%s,
                pot_telat=%s,
                pot_absen=%s,
                pot_bpjs_kes=%s,
                pot_bpjs_tk=%s,
                pot_pph21=%s,
                total_potongan=%s,
                gaji_bersih=%s
                WHERE id=%s
            """, (
                data['id_karyawan'],
                data['periode'],
                data['gaji_pokok'],
                data.get('tunj_jabatan', 0),
                hasil['upah_tetap'],
                data.get('tunj_makan', 0),
                data.get('tunj_transport', 0),
                hasil['tot_premi_kehadiran'],
                hasil['bpjs_kes_tg_perusahaan'],
                hasil['bpjs_tk_tg_perusahaan'],
                hasil['upah_penuh'],
                hasil['pot_alpha'],
                hasil['pot_telat'],
                hasil['pot_absen'],
                hasil['pot_bpjs_kes'],
                hasil['pot_bpjs_tk'],
                hasil['pph21'],
                hasil['total_potongan'],
                hasil['gaji_bersih'],
                data['id']
            ))
        db.commit()

    @staticmethod
    def delete(id):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM payroll WHERE id=%s", (id,))
        db.commit()