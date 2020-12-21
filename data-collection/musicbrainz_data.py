import psycopg2



def main():
    genres = []

    dbname = 'vibe-check'
    user = 'postgres'
    conn = psycopg2.connect(f"dbname={dbname} user={user}")
    cursor = conn.cursor()
    commit_interval = 100

    # Add genres to the database
    with open('../data/mbdump/genre', 'r') as f:
        for line in f:
            items = line.split('\t')
            genre_name = items[2]

            genres.append(genre_name)

    with open('../data/mbdump/tag') as f:
        for line in f:
            items = line.split('\t')
            tag_id = items[0]
            tag_name = items[1]

            if tag_name in genres:
                cursor.execute("INSERT INTO genre VALUES(%s, %s);", (tag_id, tag_name))

        conn.commit()

    # Create table for mb artists (might just be a dict) using mbdump/artist
    # This will have the local id and the mb_id

    # Create table for artists and their genres using mbdump/artist_tag and the genre table or array
    # This will have the mb_id and genre_id, but will be done through local id

    # Add genres to database based on mb_id (iterate through all artists from db)

        # i = 0
        # for line in f:
        #     items = line.split('\t')
        #     id = items[1]
        #     genre = items[2]
        #
        #     cursor.execute("SELECT * FROM artist WHERE mb_id = %s;", (id,))
        #     artist = cursor.fetchone()
        #     if artist is not None:
        #         artist_id = artist[0]
        #         # Add genre if it doesn't exist
        #         cursor.execute("SELECT * FROM genre WHERE genre_name = %s;", (genre,))
        #         if cursor.fetchone() is None:
        #             cursor.execute("INSERT INTO genre VALUES (%s);", (genre,))
        #
        #         cursor.execute("INSERT INTO artist_genres VALUES (%s, %s);", (artist_id, genre))
        #
        #     if i % commit_interval == 0:
        #         conn.commit()
        #         print(f'Committed {i} artist/genre pairs')






if __name__ == '__main__':
    main()