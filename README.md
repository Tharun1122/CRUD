# 🎬 Movie Catalog Web App (Flask + SQLite + OMDb API) for performing CRUD Operations

A simple Flask-based web application that allows users to manage a personal movie catalog with full **CRUD functionality** (Create, Read, Update, Delete). Users can also upload poster images or fetch them automatically using the **OMDb API**.

---

## 📌 Features

- ✅ Add new movies (with optional poster upload)
- 📖 View all movies in a responsive list
- ✏️ Edit existing movie information
- ❌ Delete movies from the catalog
- 🌐 Automatically fetch poster images using the [OMDb API](https://www.omdbapi.com/)
- 💾 Upload and serve poster images from a local `uploads/` folder

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML (Jinja2 templates)
- **External API**: OMDb API
- **Image Uploads**: Local storage

---

## 🗃️ CRUD Operations Explained

| Operation | Route                        | Description                                                                 |
|----------:|------------------------------|-----------------------------------------------------------------------------|
| **Create** | `/add`                       | Add a new movie via a form. Poster image can be uploaded (optional).       |
| **Read**   | `/`                          | Homepage displays a list of all movies in the database.                    |
| **Update** | `/edit/<int:id>`             | Edit any movie's details and update its poster image if needed.            |
| **Delete** | `/delete/<int:id>` _(POST)_ | Delete a movie and remove its associated poster image from the disk.       |

---

## 🌐 Poster Fetching (OMDb API)

- If a movie does not have a poster uploaded, you can fetch it using:
  - The `/fetch_posters` route in the app.
  - The standalone script `img.py`.
- Posters are fetched by querying OMDb API using the movie title.
- Downloaded posters are saved in the `uploads/` folder as `<id>.jpg`.

---

## 🧱 Database Schema (`movies` table)

| Column       | Type    | Description                      |
|--------------|---------|----------------------------------|
| `id`         | INTEGER | Primary key (auto-increment)     |
| `title`      | TEXT    | Movie title                      |
| `overview`   | TEXT    | Short description of the movie   |
| `release_date`| TEXT   | Release date (YYYY-MM-DD)        |
| `user_rating`| REAL    | User rating                      |
| `genres`     | TEXT    | Comma-separated genres           |
| `language`   | TEXT    | Language of the movie            |
| `adult`      | BOOLEAN | Whether it's an adult movie      |
| `poster_path`| TEXT    | File name of the poster image    |

---

## 📂 Project Structure
📁 your-project/
│
├── app.py              # Main Flask app
├── img.py              # Poster fetching script (OMDb API)
├── movies.db           # SQLite database file
├── /templates/         # HTML templates (index, add, edit)
│   ├── index.html
│   ├── add.html
│   └── edit.html
├── /uploads/           # Folder to store uploaded poster images
├── README.md           # This file

