import psycopg2

def main():
    dbname = 'vibe-check'
    user = 'postgres'
    conn = psycopg2.connect(f"dbname={dbname} user={user}")
    cursor = conn.cursor()
    commit_interval = 1000

    # Add genres to the database
    genres = []
    with open('../data/mbdump/genre', 'r') as f:
        for line in f:
            items = line.split('\t')
            genre_name = items[2]

            genres.append(genre_name)

    genre_ids = []
    with open('../data/mbdump/tag', 'r') as f:
        for line in f:
            items = line.split('\t')
            tag_id = items[0]
            tag_name = items[1]

            if tag_name in genres:
                cursor.execute("INSERT INTO genre VALUES(%s, %s);", (tag_id, tag_name))
                genre_ids.append(tag_id)

        conn.commit()

    print("Finished parsing genres")

    # Create table for mb artists (might just be a dict) using mbdump/artist
    # This will have the local id and the mb_id
    local_artist_ids = []
    with open('../data/mbdump/artist', 'r') as f:
        # Get list of mb_ids in the main artist table
        cursor.execute("SELECT mb_id FROM artist WHERE mb_id IS NOT NULL;")
        mb_id_tuples = cursor.fetchall()
        mb_ids = []
        for tuple in mb_id_tuples:
            mb_ids.append(tuple[0])

        # For artists that are in the main database, store their local musicbrainz id
        total_parsed = 0
        inserted = 0
        for line in f:
            items = line.split('\t')
            local_id = items[0]
            global_id = items[1]

            if global_id in mb_ids:
                cursor.execute("INSERT INTO mb_artist_data VALUES(%s, %s);", (global_id, local_id))
                local_artist_ids.append(local_id)
                inserted += 1

                if inserted % commit_interval == 0:
                    print(f'Inserted {inserted} artists')

            if total_parsed % commit_interval == 0:
                conn.commit()
                print(f'Parsed through {total_parsed} artists')

            total_parsed += 1

        conn.commit()

    print("Finished parsing artists")

    # Create table for artists and their genres using mbdump/artist_tag and the genre table or array
    # This will have the mb_id and genre_id, but will be done through local id
    with open('../data/mbdump/artist_tag', 'r') as f:
        total_parsed = 0
        inserted = 0
        for line in f:
            items = line.split('\t')
            artist_local_id = items[0]
            tag_id = items[1]

            if artist_local_id in local_artist_ids and tag_id in genre_ids:
                cursor.execute("SELECT a.AID FROM artist AS a JOIN mb_artist_data AS mbad ON a.mb_id = mbad.mb_global_id WHERE mbad.mb_local_id = %s;",
                               (artist_local_id,))
                aid = cursor.fetchone()[0]
                cursor.execute("INSERT INTO artist_genres VALUES(%s, %s);", (aid, tag_id))
                inserted += 1

                if inserted % commit_interval == 0:
                    print(f'Inserted {inserted} artist/genre pairs')

            if total_parsed % commit_interval == 0:
                conn.commit()
                print(f'Parsed through {total_parsed} artist/genre pairs')

            total_parsed += 1

    print("Finished creating artist/genre connections")


if __name__ == '__main__':
    main()