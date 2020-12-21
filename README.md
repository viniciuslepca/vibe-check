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

## Data Collection Stages
1. Downloaded dataset from [millionsongdataset.com](millionsongdataset.com) (~300MB)
2. Ran our [SQL Table Generator](sql/create_tables.sql)
3. Ran the [data collection script](data-collection/data_collection.py) (1 million songs, used this for most metadata about them)
4. Downloaded dataset from [musicbrainz](https://musicbrainz.org/doc/MusicBrainz_Database/Download) (~11GB)
5. 