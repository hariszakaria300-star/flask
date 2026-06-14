from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import qrcode
import base64
from io import BytesIO
from qrcode.constants import ERROR_CORRECT_H

app = Flask(__name__)

# =========================
# DATABASE SEMENTARA (RAM)
# =========================
data_pesanan = []

# =========================
# KEY FERNET (JANGAN BERUBAH)
# =========================
FERNET_KEY = b'QWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY='
cipher = Fernet(FERNET_KEY)


# =========================
# GENERATE QR CODE (FIXED)
# =========================
def generate_qr(data):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# =========================
# HALAMAN FORM
# =========================
@app.route('/')
def index():
    return render_template('form.html')


# =========================
# PROSES PESAN TIKET
# =========================
@app.route('/pesan', methods=['POST'])
def pesan():

    nama = request.form.get('nama')
    email = request.form.get('email')
    tanggal = request.form.get('tanggal_kunjungan')
    jenis = request.form.get('jenis_tiket')
    jumlah = int(request.form.get('jumlah'))

    # =========================
    # HARGA
    # =========================
    harga_satuan = 150000 if jenis == "VIP" else 100000
    total_bayar = jumlah * harga_satuan

    # =========================
    # DATA ASLI
    # =========================
    data_tiket = f"{nama}|{email}|{tanggal}|{jenis}|{jumlah}"

    # =========================
    # ENKRIPSI FERNET
    # =========================
    ciphertext = cipher.encrypt(data_tiket.encode()).decode()

    # =========================
    # QR CODE (ISI CIPHERTEXT)
    # =========================
    qr_img = generate_qr(ciphertext)

    tiket = {
        "nama": nama,
        "email": email,
        "tanggal_kunjungan": tanggal,
        "jenis_tiket": jenis,
        "jumlah": jumlah,
        "harga_satuan": harga_satuan,
        "total_bayar": total_bayar,
        "ciphertext": ciphertext,
        "qr": qr_img
    }

    data_pesanan.append(tiket)

    return render_template("tiket.html", pesanan=tiket)


# =========================
# ADMIN PAGE
# =========================
@app.route('/admin')
def admin():
    return render_template("admin.html", pesanan=data_pesanan)


# =========================
# HALAMAN VERIFIKASI
# =========================
@app.route('/verifikasi')
def verifikasi():
    return render_template("verifikasi.html")


# =========================
# PROSES DEKRIPSI
# =========================
@app.route('/cek', methods=['POST'])
def cek():

    kode = request.form.get('kode')

    try:
        hasil = cipher.decrypt(kode.encode()).decode()
        data = hasil.split('|')

        tiket = {
            "nama": data[0],
            "email": data[1],
            "tanggal": data[2],
            "jenis": data[3],
            "jumlah": data[4]
        }

        return render_template(
            "verifikasi.html",
            status="VALID",
            tiket=tiket
        )

    except:
        return render_template(
            "verifikasi.html",
            status="TIDAK VALID"
        )


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)