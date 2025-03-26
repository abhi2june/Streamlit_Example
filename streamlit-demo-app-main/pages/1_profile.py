import streamlit as st
import sqlite3
import pandas as pd

# 🎬 Set up the database
DB_FILE = "movies.db"

def create_table():
    """Initialize the database table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT, 
                    type TEXT, 
                    release_year INTEGER, 
                    age_certification TEXT, 
                    runtime INTEGER, 
                    genres TEXT, 
                    production_countries TEXT, 
                    imdb_score REAL
                 )''')
    conn.commit()
    conn.close()

create_table()

# 🎬 Fetch movies from the database
def fetch_movies():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM movies", conn)
    conn.close()
    return df

# 🎬 Insert new movie into the database
def add_movie(title, type_, release_year, age_certification, runtime, genres, production_countries, imdb_score):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO movies (title, type, release_year, age_certification, runtime, genres, production_countries, imdb_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (title, type_, release_year, age_certification, runtime, genres, production_countries, imdb_score))
    conn.commit()
    conn.close()

# 🎬 Update existing movie
def update_movie(id_, title, type_, release_year, age_certification, runtime, genres, production_countries, imdb_score):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE movies SET title=?, type=?, release_year=?, age_certification=?, runtime=?, genres=?, production_countries=?, imdb_score=? WHERE id=?",
              (title, type_, release_year, age_certification, runtime, genres, production_countries, imdb_score, id_))
    conn.commit()
    conn.close()

# 🎬 Delete movie
def delete_movie(id_):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM movies WHERE id=?", (id_,))
    conn.commit()
    conn.close()

st.title("🎬 Movie Management System")

# Fetch & Display movies
movies_df = fetch_movies()

if not movies_df.empty:
    # Group movies by release year
    grouped = movies_df.groupby("release_year")

    for year, movies in grouped:
        with st.expander(f"📅 {year} ({len(movies)} Movies)", expanded=False):
            edited_movies = st.data_editor(movies, num_rows="dynamic")

            # Save updated data
            for _, row in edited_movies.iterrows():
                update_movie(row['id'], row['title'], row['type'], row['release_year'], row['age_certification'],
                             row['runtime'], row['genres'], row['production_countries'], row['imdb_score'])

            # Delete button for each movie
            for _, row in movies.iterrows():
                if st.button(f"❌ Delete {row['title']}", key=f"del_{row['id']}"):
                    delete_movie(row['id'])
                    st.data_editor()

# 🎬 Add new movie section
st.subheader("➕ Add a New Movie")
with st.form("add_movie_form"):
    title = st.text_input("Title")
    type_ = st.selectbox("Type", ["MOVIE", "SHOW"])
    release_year = st.number_input("Release Year", min_value=1900, max_value=2030)
    age_certification = st.text_input("Age Certification")
    runtime = st.number_input("Runtime (minutes)", min_value=0)
    genres = st.text_input("Genres (comma-separated)")
    production_countries = st.text_input("Production Countries (comma-separated)")
    imdb_score = st.number_input("IMDb Score", min_value=0.0, max_value=10.0, step=0.1)

    submit_button = st.form_submit_button("Add Movie")

    if submit_button:
        add_movie(title, type_, release_year, age_certification, runtime, genres, production_countries, imdb_score)
        st.success(f"🎬 Movie '{title}' added successfully!")
        st.data_editor()
