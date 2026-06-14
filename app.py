from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import qrcode
import io
import base64

app = Flask(__name__)
cipher = Fernet(Fernet.generate_key())
data_pesanan = []

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/pesan', methods=['POST'])
def pesan():
    nama = request.form.get('nama')
    email = request.form.get('email')
    jenis_tiket = request.form.get('jenis_tiket')
    jumlah = int(request.form.get('jumlah', 1))
    
    harga_per_tiket = 3000000 if jenis_tiket == "Regular" else 4000000
    total = jumlah * harga_per_tiket
    
    data_pesanan.append({"nama": nama, "email": email, "tiket": jenis_tiket, "jumlah": jumlah, "total": total})
    
    data_qr = f"USER:{nama}|TYPE:{jenis_tiket}|TOTAL:{total}"
    token = cipher.encrypt(data_qr.encode())
    
    qr = qrcode.make(token.decode())
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template('tiket.html', nama=nama, email=email, jumlah=jumlah, 
                           jenis_tiket=jenis_tiket, total=total, harga=harga_per_tiket, qr=qr_base64)

@app.route('/admin')
def admin():
    return render_template('admin.html', pesanan=data_pesanan)

if __name__ == '__main__':
    app.run(debug=True)