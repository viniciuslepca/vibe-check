# qualifiers we'll consider
exc = ["like", "similar", "resembling"]
inc = ["by", "from"]
neg = ["not"]

songs = ["Humble", "Hello", "Watermelon Sugar"]
artists = ["Kendrick Lamar", "Adele", "Harry Styles"]
years = ["2017", "2015", "2019"]

inp = "like watermelon sugar"

# main function that takes in the user input and returns sql query for coorect info
# length taken into account later
def sqlFromClause(inp) :
    
    # get qualifier
    # returns tuple with the qualifier, then exc or inc depending on type of qualifier
    qual = findQual(inp)

    # if no qualifier found, bad inp
    if (qual = 0)
        return 0
        
    # split string into before and after qualifier
    splitString = inp.partition(qual[0])
        
    # check before qualifier if it's neg
    n = isneg(splitString[0])

    # find the object 
    obj = findObj(splitString[2])
    


def findQual(inp):
    in = inp.split()
    for i in in:
        if i in exc:
            return i, exc
        else if i in inc:
            return i, inc
    return 0    
    
def isneg(beg):
    in = beg.split()
    for i in in:
        if i in neg:
            return 1
    return 0  
    
def findObj(end):