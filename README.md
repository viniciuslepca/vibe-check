# Vibe Check
Create playlists based on any parameters you'd like! Our main feature is connecting songs
with a similar "vibe".

## Types of tasks
1. Make playlist based on simple characteristics (band, artist, genre, etc)
2. Make playlist based on similarity (similar to other songs, other artists, etc)
3. Informational queries
4. Interacting with an existing playlist (saving, sending to Spotify/Apple, adding/removing songs, etc)

## Running the SQL code
- Injecting into Postgres: `psql -U postgres -d vibe-check -a -f ${PATH_TO_FILE}`