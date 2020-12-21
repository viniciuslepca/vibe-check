# qualifiers we'll consider
exc = ["like", "similar", "resembling"]
inc = ["by", "from"]
neg = ["not"]



# getting the info we need from db 
select_artists = "SELECT artist_name FROM Artist"
select_songs = "SELECT song_name FROM Song"
select_years = "SELECT release_year FROM Song"
select_genres = "SELECT genre_name FROM Artist_genre"

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
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# assume this in input clause for now
inp = "like watermelon sugar"

# main function that takes in the user input and returns sql query for coorect info
# length taken into account later
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
    if ((qual[1] == "inc") and (obj[0] == "songs")):
        return 0

    return qual[1], n, obj[0], obj[1]

def find_qual(inp):
    str = inp.split()
    for i in str:
        if i in exc:
            return i, exc
        else if i in inc:
            return i, inc
    return 0    
    
def is_neg(beg):
    str = beg.split()
    for i in str:
        if i in neg:
            return 1
    return 0  
    
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

def make_query(qual, neg, type, obj) :
    if (type == "songs"):
        
    else if (type == "artists")



    return quer, n




