import h5py
import psycopg2

def zero_to_none(item):
    return item if item != 0 else None

def main():
    path = "../data/msd_summary_file.h5"

    dbname = 'vibe-check'
    user = 'postgres'
    conn = psycopg2.connect(f"dbname={dbname} user={user}")
    cursor = conn.cursor()
    commit_interval = 1000

    with h5py.File(path, "r") as f:
        # Get data from the file
        metadata = f['metadata']['songs']
        analysis = f['analysis']['songs']
        musicbrainz = f['musicbrainz']['songs']
        num_songs = metadata.shape[0]
        if num_songs != analysis.shape[0] or num_songs != musicbrainz.shape[0]:
            return "Sizes are incompatible"

        # Iterate and add to database
        for i in range(num_songs):
            song_metadata = metadata[i]
            song_analysis = analysis[i]
            song_musicbrainz = musicbrainz[i]

            title = song_metadata['title'].decode('utf-8')
            song_id = song_metadata['song_id'].decode('utf-8')
            artist_name = song_metadata['artist_name'].decode('utf-8')
            artist_id = song_metadata['artist_id'].decode('utf-8')
            artist_mbid = song_metadata['artist_mbid'].decode('utf-8')
            release_name = song_metadata['release'].decode('utf-8')
            release_id = int(song_metadata['release_7digitalid'])

            duration = zero_to_none(float(song_analysis['duration']))
            key = int(song_analysis['key'])
            loudness = float(song_analysis['loudness'])
            mode = int(song_analysis['mode'])
            tempo = float(song_analysis['tempo'])
            time_signature = int(song_analysis['time_signature'])

            year = zero_to_none(int(song_musicbrainz['year']))

            # Insert song if it doesn't exist in the db yet
            cursor.execute("SELECT * FROM song WHERE SID = %s;", (song_id,))
            if cursor.fetchone() is not None:
                continue
            cursor.execute("INSERT INTO song VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                           (song_id, duration, title, year, key, loudness, mode, tempo, time_signature))
            # Insert artist if it doesn't exist in the db yet
            cursor.execute("SELECT * FROM artist WHERE AID = %s;", (artist_id,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO artist VALUES(%s, %s, %s);", (artist_id, artist_mbid, artist_name))
            # Insert record if it doesn't exist in the db yet
            cursor.execute("SELECT * FROM record WHERE RID = %s;", (release_id, ))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO record VALUES(%s, %s);", (release_id, release_name))
            # Insert connections
            cursor.execute("INSERT INTO record_songs VALUES(%s, %s);", (song_id, release_id))

            cursor.execute("SELECT * FROM record_artist WHERE RID = %s AND AID = %s;", (release_id, artist_id))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO record_artist VALUES(%s, %s);", (release_id, artist_id))

            cursor.execute("INSERT INTO song_by VALUES(%s, %s);", (song_id, artist_id))

            # Commit every few iterations
            if i % commit_interval == 0:
                conn.commit()
                print(f'Committed {i} songs')

    # For mb_ids that are empty, make them null
    cursor.execute("UPDATE artist SET mb_id = NULL WHERE mb_id = '';")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()