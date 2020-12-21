# qualifiers we'll consider
exc = ["like", "similar", "resembling"]
inc = ["by", "from"]
neg = ["not"]

songs = ["Humble", "Hello", "Watermelon Sugar"]
artists = ["Kendrick Lamar", "Adele", "Harry Styles"]
years = ["2017", "2015", "2019"]
decs = ["1990s", "2000s", "2010s"]
genres = ["Rap", "Vocal", "Pop"]

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
            return decs, i

    # if not we need to check groups of words
    if end in artists:
        return artists, end
    if end in songs:
        return songs, end

    return 0



