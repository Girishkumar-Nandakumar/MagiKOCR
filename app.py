from flask import (
    Flask, render_template, request, send_file,
    session, redirect, url_for
)
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

import os
import sqlite3
import zipfile
import io

# --------------------
# APP CONFIG
# --------------------
app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret_key"
socketio = SocketIO(app)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
DB_NAME = 'users.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --------------------
# DATABASE
# --------------------
def get_db():
    return sqlite3.connect(DB_NAME)

# --------------------
# ROUTING / AUTH
# --------------------
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('ocr'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            db.commit()
            db.close()
            return redirect(url_for('login'))
        except:
            return "Username already exists"

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect(url_for('ocr'))

        return "Invalid credentials"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/ocr')
def ocr():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# --------------------
# WEBSOCKET OCR (REAL-TIME)
# --------------------
@socketio.on('start_ocr')
def handle_ocr(data):
    if 'user' not in session:
        emit('error', {'message': 'Unauthorized'})
        return

    files = data['files']
    language = data['language']

    for i, file in enumerate(files):
        filename = file['name']
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        emit('progress', {
            'file': filename,
            'status': f'Processing ({i+1}/{len(files)})'
        })

        extracted_text = ""

        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(file_path).convert('L')
            img = img.resize((img.width * 2, img.height * 2))
            img = img.point(lambda x: 0 if x < 140 else 255, '1')
            extracted_text = pytesseract.image_to_string(img, lang=language)

        elif filename.lower().endswith('.pdf'):
            pages = convert_from_path(file_path)
            for page in pages:
                page = page.convert('L')
                page = page.resize((page.width * 2, page.height * 2))
                page = page.point(lambda x: 0 if x < 140 else 255, '1')
                extracted_text += pytesseract.image_to_string(page, lang=language)

        result_file = os.path.join(RESULT_FOLDER, filename + ".txt")
        with open(result_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        emit('progress', {
            'file': filename,
            'status': 'Completed'
        })

    emit('finished', {'message': 'All files processed'})

# --------------------
# DOWNLOADS
# --------------------
@app.route('/download/zip')
def download_zip():
    if 'user' not in session:
        return redirect(url_for('login'))

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for file in os.listdir(RESULT_FOLDER):
            zipf.write(os.path.join(RESULT_FOLDER, file), file)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='ocr_results.zip'
    )

@app.route('/download/json')
def download_json():
    if 'user' not in session:
        return redirect(url_for('login'))

    data = {}
    for file in os.listdir(RESULT_FOLDER):
        with open(os.path.join(RESULT_FOLDER, file), encoding="utf-8") as f:
            data[file] = f.read()

    return data

# --------------------
# RUN APP
# --------------------
if __name__ == '__main__':
    socketio.run(app, debug=True)
