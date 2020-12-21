import os
import string
import random

import psycopg2
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

from nlp_code import query_from_clause

app = Flask(__name__, static_folder='../../frontend/build')
CORS(app, resources={r'/*': {'origins': '*'}})

dbname = 'vibe-check'
user = 'postgres'
conn = psycopg2.connect(f"dbname={dbname} user={user}")
cursor = conn.cursor()

# this part gets initial data from db to check if input data is valid
# define function to execute SQL queries easily
# i also use this function later when running the queries based on input
def execute_read_query(query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")

# getting the info we need from db
select_artists = "SELECT DISTINCT artist_name FROM Artist;"
select_songs = "SELECT DISTINCT song_name FROM Song;"
select_years = "SELECT DISTINCT release_year FROM Song WHERE release_year IS NOT NULL;"
select_genres = "SELECT DISTINCT genre_name FROM Genre;"

# executing queries
printable = string.printable
artists = execute_read_query(select_artists)
for i in range(len(artists)):
    a = artists[i][0]
    artists[i] = ''.join(filter(lambda x: x in printable, a))
songs = execute_read_query(select_songs)
for i in range(len(songs)):
    s = songs[i][0]
    songs[i] = ''.join(filter(lambda x: x in printable, s))
years = execute_read_query(select_years)
for i in range(len(years)):
    years[i] = years[i][0]
genres = execute_read_query(select_genres)
for i in range(len(genres)):
    g = genres[i][0]
    genres[i] = ''.join(filter(lambda x: x in printable, g))

# get decades from year data
decades = []
for i in years:
    i = str(i)
    if len(i) == 4 and i[2].isnumeric():
        dec = i[2] + "0s"
        decades.append(dec)

# remove duplicates
decades = set(decades)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/playlists', methods=['POST'])
def generate_playlist():
    body = request.get_json()
    duration = body['duration']
    queries = body['queries']

    output_songs = []
    for query in queries:
        # print(query)
        result = query_from_clause(query, years, decades, songs, artists, genres)
        if result == 0:
            print('something went wrong')
            continue
        else:
            is_negative = result[1]
            result = result[0]
        try:
            cursor.execute(result[0], result[1])
            output_songs = cursor.fetchall()
            # print(output_songs)
        except Exception:
            conn.rollback()

    # randomly order output
    random.shuffle(output_songs)

    # take duration into account
    final_playlist = []
    total_duration = 0
    for song in output_songs:
        final_playlist.append(song)
        song_duration = song[1]
        total_duration += song_duration
        if total_duration > duration:
            break

    return jsonify(final_playlist)

if __name__ == '__main__':
    app.run(debug=True)
