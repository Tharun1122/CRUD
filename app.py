from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import sqlite3
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Configuration
API_KEY = '1b5d978'  # Replace with your OMDb API key
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DATABASE = 'movies.db'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        overview = request.form['overview']
        release_date = request.form['release_date']
        user_rating = request.form['user_rating']
        genres = request.form['genres']
        language = request.form['language']
        adult = request.form.get('adult') == 'on'
        
        poster_path = None
        file = request.files.get('poster_path')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            poster_path = filename

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO movies (title, overview, release_date, user_rating, genres, language, adult, poster_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, overview, release_date, user_rating, genres, language, adult, poster_path))
        conn.commit()
        conn.close()
        flash("Movie added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        overview = request.form['overview']
        release_date = request.form['release_date']
        user_rating = request.form['user_rating']
        genres = request.form['genres']
        language = request.form['language']
        adult = request.form.get('adult') == 'on'

        poster_path = movie['poster_path']
        file = request.files.get('poster_path')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            poster_path = filename

        conn.execute('''
            UPDATE movies SET title = ?, overview = ?, release_date = ?, user_rating = ?, genres = ?, language = ?, adult = ?, poster_path = ?
            WHERE id = ?
        ''', (title, overview, release_date, user_rating, genres, language, adult, poster_path, id))
        conn.commit()
        conn.close()
        flash("Movie updated successfully!", "success")
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', movie=movie)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (id,)).fetchone()
    if movie['poster_path']:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], movie['poster_path']))
        except FileNotFoundError:
            pass
    conn.execute('DELETE FROM movies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Movie deleted successfully!", "info")
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/fetch_posters')
def fetch_posters():
    conn = get_db_connection()
    cursor = conn.cursor()
    movies = cursor.execute('SELECT * FROM movies').fetchall()
    updated_count = 0

    for movie in movies:
        if movie['poster_path']:
            continue  # Skip if already has an image

        title = movie['title']
        params = {
            't': title,
            'apikey': API_KEY
        }
        response = requests.get('http://www.omdbapi.com/', params=params)
        data = response.json()

        poster_url = data.get('Poster')
        if poster_url and poster_url != 'N/A':
            image_response = requests.get(poster_url)
            if image_response.status_code == 200:
                filename = secure_filename(f"{movie['id']}.jpg")
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                cursor.execute("UPDATE movies SET poster_path = ? WHERE id = ?", (filename, movie['id']))
                updated_count += 1

    conn.commit()
    conn.close()
    flash(f"Posters fetched for {updated_count} movies!", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
