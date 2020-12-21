# qualifiers we'll consider
sim = ["like", "similar", "resembling"]
sam = ["by", "from"]
neg = ["not"]



# this part gets inital data from db to check if input data is valid

# getting the info we need from db 
select_artists = "SELECT artist_name FROM Artist"
select_songs = "SELECT song_name FROM Song"
select_years = "SELECT release_year FROM Song"
select_genres = "SELECT genre_name FROM Artist_genre"
# executing queries
artists = execute_read_query(connection, select_artists)
songs = execute_read_query(connection, select_songs)
years = execute_read_query(connection, select_years)
genres = execute_read_query(connection, select_genres)


# get decades from year data
for i in years:
    if len(i) == 4 :
        dec = i[2:3] + "s"
        decades.append(dec)

# remove duplicates
decades = set(decades)


# define function to execute SQL queries easily
# i also use this function later when running the queries based on input
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")







# this part converts the language query into a tuple 

# assume this in input clause for now
inp = "like watermelon sugar"


# function that takes in the user input clause and returns 4-tuple of 
# sim/sam neg/pos years/artists/songs/decades name
# after this info is extracted from input we can determine which SQL query to run
def query_from_clause(inp) :
    
    # get qualifier
    # returns tuple with the qualifier, then exc or inc depending on type of qualifier
    qual = find_qual(inp)

    # if no qualifier found, bad inp
    if (qual = 0)
        return 0
        
    # split string into before and after qualifier
    split_string = inp.partition(qual[0])
        
    # check before qualifier if it's neg
    n = is_neg(splitString[0])

    # find the object 
    obj = find_obj(splitString[2])

    # user can't ask for from or by a song
    if ((qual[1] == "sam") and (obj[0] == "songs")):
        return 0

    return qual[1], n, obj[0], obj[1]

# query_from_clause helper to get qualifier type
def find_qual(inp):
    str = inp.split()
    for i in str:
        if i in sam:
            return i, sam
        else if i in sim:
            return i, sim
    return 0    
    
# query_from_clause helper to get if request is negative
def is_neg(beg):
    str = beg.split()
    for i in str:
        if i in neg:
            return 1
    return 0  
    
# query_from_clause helper to get type of object and object name
def find_obj(end):
    str = end.split()
    # check if a year or decade
    for i in str:
        if i in years:
            return years, i
        if i in decs:
            return decades, i

    # if not we need to check groups of words
    if end in artists:
        return artists, end
    if end in songs:
        return songs, end

    # should check if we should put this first perhaps?
    if end in genres:
        return genres, end

    return 0







# this part takes in the 4-tuple and executes the correct query as a result
# this does not take into account if query is neg, rather it returns a 2-tuple 
# with the query results and if they're negative so we can negate in the query aggragation phase
# gives query from one clause
def make_query(qual, neg, type, obj) :
    # for queries askign for the same
    if (qual == "sam"):
	if (type == "artists"):
            ask = ("SELECT Song.song_name, Artist.artist_name, Song.release_year
		FROM Song, Song_By, Artist
		WHERE Song.sid = Song_By.sid AND
			Song_By.arid = Artist.alid AND
     		        Artist.artist_name = %s;", obj)
	else if (type == "years"):
            ask = ("SELECT Song.song_name, Artist.artist_name, Song.release_year
		FROM Song, Song_By, Artist
		WHERE Song.sid = Song_By.sid AND
			Song_By.arid = Artist.alid AND
     		        Song.release_year = %s;", obj)
	else if (type == "decades"):
	    # get bounds of decade to compare in sql query
	    dec = obj[0:1]
	    if (int(dec[0]) < 3) :
		dec = int("19" + dec)
            else :
		dec = int("20" + dec)
	
            beg = dec
	    end = dec + 9

            ask = ("SELECT Song.song_name, Artist.artist_name, Song.release_year
		FROM Song, Song_By, Artist
		WHERE Song.sid = Song_By.sid AND
			Song_By.aid = Artist.aid AND
     		        release_year <= %s AND 
                        release_year >= %s;", (end, beg))


    # for queries asking for similar
    else if (qual == "sim"):
        if (type == "songs"):

	else if (type == "artists"):

	else if (type == "years"):
            ask = ("SELECT s2.song_name, Artist.artist_name, s2.release_year
		FROM Song s1, Song s2, Song_By, Artist
		WHERE s2.release_year >= s1.release_year - 3 AND
			s2.release_year <= s1.release_year + 3 AND
			Song_By.aid = Artist.aid AND
			s1.song_name = name AND
			s1.release_year = %s AND
			Song_By.sid = s2.sid;", obj)

	else if (type == "decades"):
	    # get bounds of decade to compare in sql query
	    dec = obj[0:1]
	    if (int(dec[0]) < 3) :
		dec = int("19" + dec)
            else :
		dec = int("20" + dec)
	
            beg = dec
	    end = dec + 9

            ask = ("SELECT Song.song_name, Artist.artist_name, Song.release_year
		FROM Song, Song_By, Artist
		WHERE Song.sid = Song_By.sid AND
			Song_By.aid = Artist.aid AND
     		        release_year <= %s AND 
                        release_year >= %s;", (end, beg))

    quer = execute_read_query(connection, ask)


    return quer, n





# function for query aggregation
# based on a list of quers and their neg/pos boolean, we union/intersect the queries to produce our
# final query over multiple clauses




