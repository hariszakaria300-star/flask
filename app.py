from flask import Flask, render_template, request

app = Flask(__name__)

history = []

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        namaDepan = request.form['namaDepan']
        namaBelakang = request.form['namaBelakang']

        nama = namaDepan + " " + namaBelakang

        hasil = ""

        k = 3

        for huruf in nama:

            if huruf == " ":
                hasil += " "

            else:
                hasil += chr(ord(huruf) + k)

        history.append({
            'asli': nama,
            'encrypt': hasil
        })

        return render_template(
            'response.html',
            nama=hasil
        )

    return render_template('form.html')


@app.route('/history')
def riwayat():

    return render_template(
        'history.html',
        history=history
    )


@app.route('/clear-history')
def clear_history():

    history.clear()

    return render_template(
        'history.html',
        history=history
    )


if __name__ == '__main__':
    app.run(debug=True)