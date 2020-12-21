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
5. Ran the [musicbrainz data collection script](data-collection/musicbrainz_data.py) (populates data about artists and genres, about 38k artists)

## How to execute
1. Run `sql/create_tables.sql` using `psql -U postgres -d vibe-check -a -f ${PATH_TO_FILE}`
2. From `/data-collection`, run `data_collection.py`
3. From `/data-collection`, run `musicbraiz_data.py`
4. Install requirements (on virtual environments): from root, run `pip install -r requirements.txt`
5. From `/backend`, run `python3 app.py`
6. With another terminal, from `/frontend` run `npm install` then `npm start`
7. Access through `localhost:3000`