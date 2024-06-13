from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import mysql.connector
import os
import hashlib
import pandas as pd
import csv

app = Flask(__name__)

# Set kunci rahasia
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="data_guru"
)

# Inisialisasi stemmer
stemmer = PorterStemmer()

# Inisialisasi vektor fitur dengan CountVectorizer
vectorizer = CountVectorizer()

# Melakukan tokenisasi, stemming, dan pre-processing pada teks
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)

# Fungsi untuk melakukan hash pada password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi untuk menganalisis pengalaman guru
def analyze_experience(sentence):
    # Membaca dataset dan mendapatkan kata kunci beserta labelnya dari setiap baris
    df = pd.read_csv('dataset.csv')
    kata_kunci = df[['pengalaman', 'label']].values.tolist()

    unique_labels = set()
    fulfilled_parameters = set()

    for keywords, label in kata_kunci:
        # Split kata kunci menjadi sebuah list
        keyword_list = keywords.split(', ')
        # Hitung jumlah kata kunci yang terdapat dalam kalimat pengalaman
        count_keywords = sum(keyword.lower() in sentence.lower() for keyword in keyword_list)
        # Periksa apakah semua label dari kata kunci tersebut adalah 'guru penggerak telah melakukan perannya dengan baik'
        if count_keywords >= 4 and all(label.lower() == 'guru penggerak telah melakukan perannya dengan baik' for label in keyword_list):
            fulfilled_parameters.add(keywords)
            unique_labels.add(label)
        # Periksa apakah kata kunci yang bersangkut paut dengan kata kunci dalam kalimat
        if all(keyword.lower() in sentence.lower() for keyword in keyword_list):
            fulfilled_parameters.add(keywords)
            unique_labels.add(label)

    # Tentukan hasil berdasarkan jumlah label dan parameter yang terpenuhi
    if len(unique_labels) == 1 and len(fulfilled_parameters) >= 4:
        return "Guru penggerak telah melakukan perannya dengan baik"
    else:
        return "Guru penggerak belum melakukan perannya secara optimal"


# Render halaman welcome
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Render halaman login
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    # Cari user berdasarkan username dalam database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    # Jika user ditemukan dan password cocok
    if user and user[2] == hash_password(password):
        # Login berhasil, simpan status login dalam sesi
        session['logged_in'] = True
        return redirect(url_for('home'))
    else:
        # Login gagal, kirim respon dengan status HTTP 401 (Unauthorized)
        return jsonify({'error': 'Username atau password salah'}), 401

# Menampilkan formulir register
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']

    # Hash password sebelum menyimpannya ke database
    hashed_password = hash_password(password)

    # Cek apakah username sudah ada dalam database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        return render_template('register.html', error='Username sudah digunakan. Silakan pilih username lain.')
    
    # Jika username belum ada, lakukan registrasi
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    db.commit()
    cursor.close()

    # Redirect ke halaman login setelah registrasi berhasil
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'logged_in' in session and session['logged_in']:
        # Mengambil jumlah user dari tabel users
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        jumlah_user = cursor.fetchone()[0]
        cursor.close()

        # Mengambil jumlah prediksi dari tabel predictions
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM predictions")
        total_predictions = cursor.fetchone()[0]
        cursor.close()

        # Menghitung jumlah prediksi berdasarkan kategori
        cursor = db.cursor()
        cursor.execute(
            "SELECT prediction, COUNT(*) AS count FROM predictions WHERE prediction = 'Guru penggerak telah melakukan perannya dengan baik' OR prediction = 'Guru penggerak belum melakukan perannya secara optimal' GROUP BY prediction")
        prediction_counts = cursor.fetchall()
        cursor.close()

        return render_template('index.html', jumlah_user=jumlah_user, total_predictions=total_predictions, prediction_counts=prediction_counts)
    else:
        return redirect(url_for('login'))


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_name = request.form['name']
        input_nip = request.form['nip']
        input_school = request.form['school']
        input_sentence = request.form['sentence']

        # Pre-processing pada kalimat uji
        preprocessed_sentence = preprocess_text(input_sentence)

        # Melakukan ekstraksi fitur pada kalimat uji
        test_features = vectorizer.transform([preprocessed_sentence])

        # Melakukan prediksi dengan model Naive Bayes
        prediction = naive_bayes_classifier.predict(test_features)

        # Menyimpan data prediksi ke database
        save_prediction(input_name, input_nip, input_school, input_sentence, prediction[0])

        if prediction[0] == "Guru penggerak telah melakukan perannya dengan baik":
            result = "Guru penggerak telah melakukan perannya dengan baik."
        else:
            result = "Guru penggerak belum melakukan perannya secara optimal."

        return jsonify({'prediction_result': result})

@app.route('/hasil_prediksi')
def hasil_prediksi():
    cursor = db.cursor()
    cursor.execute("SELECT name, nip, school, sentence, prediction FROM predictions ORDER BY id DESC")
    predictions = cursor.fetchall()
    cursor.close()
    return render_template('hasil_prediksi.html', predictions=predictions)

@app.route('/prediksi')
def prediksi():
    return render_template('prediksi.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename.endswith('.csv'):
        try:
            data = pd.read_csv(file)
            required_columns = {'name', 'nip', 'school', 'pengalaman'}
            if not required_columns.issubset(data.columns):
                return jsonify({'error': f'CSV file must contain the following columns: {required_columns}'}), 400
        except Exception as e:
            return jsonify({'error': f'Error reading CSV file: {e}'}), 400

        try:
            data['prediction'] = data['pengalaman'].apply(lambda x: naive_bayes_classifier.predict(vectorizer.transform([preprocess_text(x)]))[0])
        except Exception as e:
            return jsonify({'error': f'Error processing predictions: {e}'}), 400

        uploaded_data = data.to_dict(orient='records')

        cursor = db.cursor()
        for index, row in data.iterrows():
            try:
                sql = "INSERT INTO predictions (name, nip, school, sentence, prediction) VALUES (%s, %s, %s, %s, %s)"
                val = (row['name'], row['nip'], row['school'], row['pengalaman'], row['prediction'])
                cursor.execute(sql, val)
            except Exception as e:
                print(f"Error saving row {index}: {e}")
        db.commit()
        cursor.close()

        return jsonify({'message': 'File uploaded successfully', 'uploaded_data': uploaded_data})
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/delete_all_predictions', methods=['DELETE'])
def deleteAllPredictions():
    cursor = db.cursor()
    cursor.execute("DELETE FROM predictions")
    db.commit()
    cursor.close()
    return ('', 204)

def save_prediction(name, nip, school, sentence, prediction):
    cursor = db.cursor()
    sql = "INSERT INTO predictions (name, nip, school, sentence, prediction) VALUES (%s, %s, %s, %s, %s)"
    val = (name, nip, school, sentence, prediction)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()

@app.route('/export', methods=['GET'])
def export():
    cursor = db.cursor()
    cursor.execute("SELECT name, nip, school, sentence, prediction FROM predictions")
    predictions = cursor.fetchall()
    cursor.close()

    # Nama file CSV yang akan diekspor
    csv_file = 'predictions.csv'

    # Menulis data ke file CSV
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'NIP', 'School', 'Sentence', 'Prediction'])
        writer.writerows(predictions)

    return send_file(csv_file, as_attachment=True, download_name=csv_file)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('welcome'))

# Load dataset dari file CSV
df = pd.read_csv('dataset.csv')
training_sentences = df['pengalaman'].tolist()
training_labels = df['label'].tolist()

training_sentences_preprocessed = [preprocess_text(sentence) for sentence in training_sentences]
training_features = vectorizer.fit_transform(training_sentences_preprocessed)

naive_bayes_classifier = MultinomialNB()
naive_bayes_classifier.fit(training_features, training_labels)

if __name__ == '__main__':
    app.run(debug=True)
