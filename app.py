from flask import Flask, render_template, g, request
import sqlite3
import os

app = Flask(__name__)

# --- Konfigurasi Database ---
DATABASE = os.path.join(os.getcwd(), 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Inisialisasi Database ---
def init_db():
    with app.app_context():
        db = get_db()
        cur = db.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS wisata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            deskripsi_singkat TEXT,
            deskripsi_lengkap TEXT,
            gambar TEXT
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS makanan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            deskripsi TEXT,
            gambar TEXT
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS bahan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            makanan_id INTEGER,
            nama_bahan TEXT,
            FOREIGN KEY (makanan_id) REFERENCES makanan(id)
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS tutorial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            makanan_id INTEGER,
            langkah TEXT,
            FOREIGN KEY (makanan_id) REFERENCES makanan(id)
        )
        ''')

        # Tambahkan data wisata
        cur.executescript('''
                INSERT INTO wisata (nama, deskripsi_singkat, deskripsi_lengkap, gambar) VALUES
                ('Pantai Ngurbloat', 'Pantai dengan pasir sehalus tepung.', 'Pantai Ngurbloat dikenal memiliki pasir putih yang sangat halus, bahkan seperti tepung. Air lautnya jernih dan cocok untuk berenang, bersantai, serta menikmati sunset yang indah.', 'files/ngurbloat.jpg'),
                ('Pulau Bair', 'Pulau dengan air jernih dan tebing indah.', 'Pulau Bair sering disebut sebagai "Raja Ampat Mini" karena memiliki air laut yang sangat jernih, tebing karst yang menjulang tinggi, serta suasana yang masih alami. Tempat ini cocok untuk snorkeling dan fotografi alam.', 'files/bair.jpg'),
                ('Goa Hawang', 'Gua unik dengan air biru jernih.', 'Goa Hawang adalah gua bawah tanah yang memiliki kolam air alami yang sangat jernih. Tempat ini dikelilingi mitos yang menarik dari masyarakat lokal.', 'files/hawang.jpg');

                INSERT INTO makanan (nama, deskripsi, gambar) VALUES
                ('Enbal', 'Makanan tradisional berbahan dasar singkong yang dikeringkan dan difermentasi.', 'files/enbal.png'),
                ('Ikan Bakar Kei', 'Ikan segar yang dibakar dengan bumbu khas Kepulauan Kei.', 'files/ikan_bakar.png'),
                ('Ikan Kuah Kuning', 'Ikan segar dimasak dengan kuah kuning berbumbu khas.', 'files/ikan_kuah_kuning.png'),
                ('Sayur Sir-Sir', 'Sayur khas Kei yang berbahan dasar daun kelor dan santan.', 'files/sayur sir-sir.png'),
                ('Pisang Enbal', 'Pisang yang diolah dengan enbal untuk cita rasa khas.', 'files/pisang_enbal.png'),
                ('Lat / Anggur Laut', 'Rumput laut alami yang kaya akan nutrisi dan sering dikonsumsi sebagai lalapan.', 'files/lat_anggur_laut.png');

                INSERT INTO bahan (makanan_id, nama_bahan) VALUES
                (1, 'Singkong secukupnya'),
                (1, 'Air untuk mencuci dan merendam'),

                (2, '1 ekor ikan segar (kakap/tuna atau sesuai selera)'),
                (2, '2 siung bawang merah'),
                (2, '2 siung bawang putih'),
                (2, '1 ruas kunyit'),
                (2, '1 sdt garam'),
                (2, '1 buah jeruk nipis'),
                (2, 'Minyak secukupnya'),

                (3, '1 ekor ikan segar (kakap/tuna atau sesuai selera)'),
                (3, '3 siung bawang merah'),
                (3, '2 siung bawang putih'),
                (3, '1 ruas kunyit'),
                (3, '2 butir kemiri'),
                (3, '1 ruas jahe'),
                (3, '2 lembar daun jeruk'),
                (3, '1 batang serai, memarkan'),
                (3, '500 ml air'),
                (3, '1 sdt garam'),
                (3, '1 sdt air jeruk nipis'),

                (4, '1 ikat daun kelor'),
                (4, '3 siung bawang merah'),
                (4, '2 siung bawang putih'),
                (4, '2 buah cabai merah'),
                (4, '200 ml santan'),
                (4, '1 sdt garam'),

                (5, '3 buah pisang matang'),
                (5, '100 gram enbal kering'),
                (5, 'Minyak goreng secukupnya'),

                (6, '200 gram lat/anggur laut'),
                (6, 'Air hangat untuk merendam');

                INSERT INTO tutorial (makanan_id, langkah) VALUES
                (1, 'Kupas dan cuci bersih singkong.'),
                (1, 'Parut singkong hingga halus.'),
                (1, 'Peras singkong untuk menghilangkan racun sianida.'),
                (1, 'Keringkan di bawah sinar matahari selama beberapa hari.'),
                (1, 'Enbal siap diolah atau disimpan untuk penggunaan selanjutnya.'),

                (2, 'Bersihkan ikan dan lumuri dengan air jeruk nipis.'),
                (2, 'Haluskan bawang merah, bawang putih, kunyit, dan garam.'),
                (2, 'Balurkan bumbu ke seluruh bagian ikan.'),
                (2, 'Bakar ikan di atas arang sambil sesekali dibalik hingga matang.'),
                (2, 'Sajikan dengan sambal dan nasi hangat.'),

                (3, 'Bersihkan ikan dan potong sesuai selera.'),
                (3, 'Haluskan kunyit, bawang merah, bawang putih, kemiri, dan jahe.'),
                (3, 'Tumis bumbu halus hingga harum.'),
                (3, 'Tambahkan air dan masukkan daun jeruk serta serai.'),
                (3, 'Masukkan ikan dan masak hingga matang.'),
                (3, 'Tambahkan garam dan perasan jeruk nipis, lalu sajikan.'),

                (4, 'Petik daun kelor dari tangkainya dan cuci bersih.'),
                (4, 'Iris bawang merah, bawang putih, dan cabai.'),
                (4, 'Tumis bumbu hingga harum, lalu tambahkan santan.'),
                (4, 'Masukkan daun kelor dan aduk perlahan.'),
                (4, 'Masak hingga daun layu, kemudian sajikan.'),

                (5, 'Kupas pisang dan iris tipis.'),
                (5, 'Campurkan dengan enbal yang sudah dihaluskan.'),
                (5, 'Goreng hingga kecoklatan dan renyah.'),
                (5, 'Tiriskan dan sajikan sebagai camilan.'),

                (6, 'Cuci bersih lat/anggur laut dengan air tawar.'),
                (6, 'Rendam sebentar dalam air hangat untuk menghilangkan garam.'),
                (6, 'Sajikan dengan sambal dan lauk lainnya.');
                ''')

        db.commit()

# --- ROUTE Halaman utama ---
@app.route('/')
def home():
    return render_template('index.html')

# --- ROUTE Wisata ---
@app.route('/wisata')
def wisata():
    db = get_db()
    data = db.execute('SELECT * FROM wisata').fetchall()
    return render_template('wisata.html', wisata_list=data)

@app.route('/wisata/<int:id>')
def wisata_detail(id):
    db = get_db()
    wisata = db.execute('SELECT * FROM wisata WHERE id = ?', (id,)).fetchone()
    if not wisata:
        return "Wisata tidak ditemukan", 404
    return render_template('detail_wisata.html', wisata=wisata)

# --- ROUTE Makanan ---
@app.route('/makanan')
def makanan():
    db = get_db()
    data = db.execute('SELECT * FROM makanan').fetchall()
    return render_template('makanan.html', makanan_list=data)

@app.route('/makanan/<int:id>')
def makanan_detail(id):
    db = get_db()
    makanan = db.execute('SELECT * FROM makanan WHERE id = ?', (id,)).fetchone()
    if not makanan:
        return "Makanan tidak ditemukan", 404

    bahan = db.execute('SELECT nama_bahan FROM bahan WHERE makanan_id = ?', (id,)).fetchall()
    tutorial = db.execute('SELECT langkah FROM tutorial WHERE makanan_id = ?', (id,)).fetchall()

    return render_template('detail_makanan.html', makanan=makanan, bahan=bahan, tutorial=tutorial)

# --- ROUTE Informasi ---
@app.route('/sejarah')
def sejarah():
    return render_template('sejarah.html')

@app.route('/geografi')
def geografi():
    return render_template('geografi.html')

@app.route('/demografi')
def demografi():
    return render_template('demografi.html')

@app.route('/footer')
def footer():
    return render_template('footer_section.html')

# --- Jalankan Aplikasi ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0")
