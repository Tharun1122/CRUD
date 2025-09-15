import requests
import sqlite3
import os

API_KEY = '1b5d978'  # Replace with your actual OMDb API key
UPLOAD_FOLDER = 'uploads'

# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Connect to the database
conn = sqlite3.connect('movies.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Fetch all movies
cursor.execute("SELECT id, title FROM movies")
movies = cursor.fetchall()

for movie in movies:
    title = movie['title']
    image_filename = f"{movie['id']}.jpg"
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)

    if os.path.exists(image_path):
        continue  # Skip if image already exists

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
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
            cursor.execute("UPDATE movies SET poster_path = ? WHERE id = ?", (image_filename, movie['id']))
            print(f"Downloaded poster for {title}")

# Commit changes and close the connection
conn.commit()
conn.close()
