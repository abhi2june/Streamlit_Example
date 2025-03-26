import streamlit as st
import pandas as pd

# Load data
data = pd.read_csv("movies.csv")

# Drop missing release years and convert to int
data = data.dropna(subset=['release_year'])
data['release_year'] = data['release_year'].astype(int)

# Sort by year (latest first)
data = data.sort_values(by='release_year', ascending=False)

st.title("🎬 Movies by Release Year")

# Group movies by release year
grouped_data = data.groupby("release_year")

# Store edited data
updated_data = []

# Iterate through each year and display movies
for year, movies in grouped_data:
    with st.expander(f"📅 {year} ({len(movies)} Movies)", expanded=False):
        edited_movies = st.data_editor(movies, num_rows="dynamic")
        updated_data.append(edited_movies)

# Combine all edited data
final_data = pd.concat(updated_data)

# Download updated data
st.download_button(
    label="⬇️ Download Updated Movies",
    data=final_data.to_csv(index=False),
    file_name="updated_movies.csv",
    mime="text/csv"
)
