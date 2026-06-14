from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
data_pesanan = []

def generate_qr(data):
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/pesan', methods=['POST'])
def pesan():
    nama = request.form.get('nama')
    email = request.form.get('email')
    tanggal = request.form.get('tanggal_kunjungan')
    jenis = request.form.get('jenis_tiket')
    jumlah = request.form.get('jumlah')
    
    # Data untuk QR (ini yang akan dibaca scanner nantinya)
    isi_qr = f"Tiket: {nama} | {tanggal} | {jenis} | {jumlah} tiket"
    qr_img = generate_qr(isi_qr)
    
    tiket = {
        'nama': nama, 'email': email, 'tanggal_kunjungan': tanggal,
        'jenis_tiket': jenis, 'jumlah': jumlah, 'qr': qr_img
    }
    
    data_pesanan.append(tiket)
    return render_template('tiket.html', pesanan=tiket)

@app.route('/admin')
def admin():
    return render_template('admin.html', pesanan=data_pesanan, enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)