# this part converts the language query into a tuple

# qualifiers we'll consider
sim = ["Like", "Similar", "Resembling"]
sam = ["By", "From"]
neg = ["Not"]

# function that takes in the user input clause and returns 4-tuple of
# sim/sam neg/pos years/artists/songs/decades name
# after this info is extracted from input we can determine which SQL query to run
def query_from_clause(inp, years, decades, songs, artists, genres) :

    # get qualifier
    # returns tuple with the qualifier, then exc or inc depending on category of qualifier
    inp = inp.title()
    qual = find_qual(inp)
    print(qual)

    # if no qualifier found, bad inp
    if qual == 0:
        return 0

    # split string into before and after qualifier
    split_string = inp.partition(qual[0])

    # check before qualifier if it's neg
    n = is_neg(split_string[0])

    # find the object
    obj = find_obj(split_string[2].strip(), years, decades, songs, artists, genres)
    print(obj)

    # user can't ask for from or by a song
    if (qual[1] == "sam") and (obj[0] == "songs"):
        return 0

    print(qual[1], n, obj[0], obj[1])
    return make_query(qual[1], n, obj[0], obj[1])

# query_from_clause helper to get qualifier category
def find_qual(inp):
    string = inp.split()
    for c in string:
        if c in sam:
            return c, "sam"
        elif c in sim:
            return c, "sim"
    return 0

# query_from_clause helper to get if request is negative
def is_neg(beg):
    string = beg.split()
    for c in string:
        if c in neg:
            return 1
    return 0

# query_from_clause helper to get category of object and object name
def find_obj(end, years, decades, songs, artists, genres):
    items = end.split()
    print(items)
    # check if a year or decade
    for c in items:
        if c in decades:
            return "decades", c
        if c.isnumeric():
            c = int(c)
            if c in years:
                return "years", c

    # if not we need to check groups of words
    if end in artists:
        return "artists", end
    if end in songs:
        return "songs", end

    # should check if we should put this first perhaps?
    if end in genres:
        return "genres", end

    return 0, 0

# this part takes in the 4-tuple and executes the correct query as a result
# this does not take into account if query is neg, rather it returns a 2-tuple
# with the query results and if they're negative so we can negate in the query aggregation phase
# gives query from one clause
def make_query(qual, n, category, obj) :
    # for queries asking for the same
    if qual == "sam":
        if category == "artists":
            ask = ("""SELECT Song.song_name, Song.length, Artist.artist_name, Song.release_year
            FROM Song, Song_By, Artist
            WHERE Song.sid = Song_By.sid AND
                Song_By.aid = Artist.aid AND
                        Artist.artist_name = %s;""", (obj,))
        elif category == "years":
            ask = ("""SELECT Song.song_name, Song.length, Artist.artist_name, Song.release_year
            FROM Song, Song_By, Artist
            WHERE Song.sid = Song_By.sid AND
                Song_By.aid = Artist.aid AND
                        Song.release_year = %s;""", (obj,))
        elif category == "decades":
            # get bounds of decade to compare in sql query
            dec_val = obj[0:1]
            if int(dec_val[0]) < 3 :
                dec_val = int("19" + dec_val)
            else :
                dec_val = int("20" + dec_val)

            beg = dec_val
            end = dec_val + 9

            ask = ("""SELECT Song.song_name, Song.length, Artist.artist_name, Song.release_year
            FROM Song, Song_By, Artist
            WHERE Song.sid = Song_By.sid AND
                Song_By.aid = Artist.aid AND
                        release_year <= %s AND
                            release_year >= %s;""", (end, beg))

        else:
            return 0


    # for queries asking for similar
    elif qual == "sim":
        if category == "songs":
            ask = ("""SELECT s2.song_name, s2.length, Artist.artist_name, s2.release_year
            FROM Song s1, Song s2, Song_By sb1, Song_By sb2, Artist
            WHERE s1.sid = sb1.sid AND
                sb1.aid = sb2.aid AND
                        s2.sid = sb2.sid AND
                s1.song_name = %s AND
                sb2.aid = Artist.aid
            UNION
                    -- sim year
            SELECT s2.song_name, s2.length, Artist.artist_name, s2.release_year
            FROM Song s1, Song s2, Song_By, Artist
            WHERE s2.release_year >= s1.release_year - 2 AND
                s2.release_year <= s1.release_year + 2 AND
                Song_By.aid = Artist.aid AND
                s1.song_name = %s AND
                Song_By.sid = s2.sid
            UNION
                    -- same genre
            SELECT s2.song_name, s2.length, a2.artist_name, s2.release_year
            FROM Song s1, Song s2, Song_By sb1, Song_By sb2, Artist a1, Artist a2, Artist_Genres ag1, Artist_Genres ag2
            WHERE s1.sid = sb1.sid AND
                s2.sid = sb2.sid AND
                sb1.aid = a1.aid AND
                sb2.aid = a2.aid AND
                a1.aid = ag1.aid AND
                a2.aid = ag2.aid AND
                s1.song_name = %s AND
                ag1.gid = ag2.gid;""", (obj, obj, obj))

        elif category == "artists":
            ask = ("""SELECT Song.song_name, Song.length, Artist.artist_name, Song.release_year
            FROM Song, Song_By, Artist
            WHERE Song.sid = Song_By.sid AND
                Artist.artist_name = %s AND
                Song_By.aid = Artist.aid
            UNION
            -- sim year
            SELECT s2.song_name, s2.length, Artist.artist_name, s2.release_year
            FROM Song s1, Song s2, Song_By, Artist
            WHERE s1.sid = Song_By.sid AND
                Song_By.aid = Artist.aid AND
                Artist.artist_name = %s AND
                s2.release_year >= (SELECT MIN(release_year) FROM s1) AND
                s2.release_year <= (SELECT MAX(release_year) FROM s1)
            UNION
            -- same genre
            SELECT Song.song_name, Song.length, A2.artist_name, Song.release_year
            FROM Song, Song_By, Artist a1, Artist a2, Artist_Genres ag1, Artist_Genres ag2
            WHERE a1.aid = ag1.aid AND
                a1.artist_name = %s AND
                Song.sid = Song_By.sid AND
                Song_By.aid = a2.aid AND
                a2.aid = ag2.aid AND
                ag2.gid = ag1.gid""", (obj, obj, obj))

        elif category == "years":
            ask = ("""SELECT s2.song_name, s2.length, Artist.artist_name, s2.release_year
            FROM Song s1, Song s2, Song_By, Artist
            WHERE s2.release_year >= s1.release_year - 3 AND
                s2.release_year <= s1.release_year + 3 AND
                Song_By.aid = Artist.aid AND
                s1.song_name = %s AND
                s1.release_year = %s AND
                Song_By.sid = s2.sid;""", (obj,))

        elif category == "decades":
            # get bounds of decade to compare in sql query
            dec_val = obj[0:1]
            if int(dec_val[0]) < 3:
                dec_val = int("19" + dec_val)
            else :
                dec_val = int("20" + dec_val)

            beg = dec_val
            end = dec_val + 9

            ask = ("""SELECT Song.song_name, Song.length, Artist.artist_name, Song.release_year
            FROM Song, Song_By, Artist
            WHERE Song.sid = Song_By.sid AND
                Song_By.aid = Artist.aid AND
                        release_year <= %s AND
                            release_year >= %s;""", (end, beg))

        else:
            return 0
    else:
        return 0

    return ask, n



# function for query aggregation
# based on a list of quers and their neg/pos boolean, we union/intersect the queries to produce our
# final query over multiple clauses
# def aggregate(quer[], n[]) :





