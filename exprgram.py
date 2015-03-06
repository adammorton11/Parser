
import re, sys, string
import keyword

syntaxDebug = False
tokens = ""


#  Expression class and its subclasses
class Expression( object ):
    def __str__(self):
        return ""


class BinaryExpr( Expression ):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def __str__(self):
        return str(self.op) + " " + str(self.left) + " " + str(self.right)

class Number( Expression ):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
class String( Expression ):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)    

class Variable( Expression):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)


class Assign( object):
    def __init__(self, target, source):
        self.target = target
        self.source = source

def __str__(self):
    return "= " + str(target) + " " + str(source)
class Statement( object ):
    def __str__(self):
        error("Should never be called.")

class  StmtList( Statement ):
    def __init__(self, list):
        self.list = list
    
    def __str__(self):
        out = ""
        for stmt in self.list:
            out += str(stmt) + "\n"
        return out

class While( object ):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return"\nwhile " + str(self.left) + " do" + "\n" + str(self.right) + "od"

class Od( object ):
    def __init__(self, od):
        self.od = od
    def __str__(self):
        return str(self.od)

# -----Statement Parsing Routines --------





def parseWhile():
    match('while')
    
    cond = addExpr()
    match('do')
    stmts = parseStmtList()
    match('od')
    ret = While(cond, stmts)
    
    return ret

def parseStatement():
    tok = tokens.peek()
    if tok == 'while':
        return parseWhile()
    elif tok == 'od':
        return Od(tok)
    else:
        return orExpr()



#def parseAssign():
    ## assign -> variable = addExpr ;
    #if syntaxDebug: print ("assign: ", tokens.peek())
    #target = parseVariable()
    #match("=")
    #source = addExpr()
    #match(";")
    #return Assign(target, source)




def parseStmtList():
    # stmtList = {{ assign }}
    list = []
    #tokens.tokens = [v for i, v in enumerate(tokens.tokens) if v not in tokens.special]    
    while tokens.peek() != None:
        if syntaxDebug: print ("stmtlist: ", tokens.peek())
        ast = parseStatement()
        if str(ast) == "od":
            return StmtList(list)
        list.append(ast)

    return StmtList(list)




def parseVariable():
    # variable -> identifier
    if tokens.check_key(tokens.peek):
        error("Expecting identifier, got "+tokens.peek())
    tok = tokens.peek()
    tokens.next()
    return Variable(tok)

# ---------------- Expression Classes -------------------

class Assign( Statement ):
    def __init__(self, target, source):
        self.target = target;
        self.source = source
    
    def __str__(self):
        return "= "+str(self.target)+" "+str(self.source)
def Statement(ast):
    return assign ()


def assign( ):
    # assign -> ident = expr
    target = match([ident])  # ???
    #if tokens.peekback() != "od":
    match(["="])
    source = expr( )
    return Assign(target, source)


def error( msg ):
    #print msg
    sys.exit(msg)

# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.

def match(matchtok):
    tok = tokens.peek( )
    if (tok != matchtok): error("Expecting "+ matchtok)
    tokens.next( )
    return tok


def matchAny(list):
    # tokSet = set(list)
    tok = tokens.peek()
    if tok not in list:
        error("Expecting "+", ".join(list) + ", got "+tok)
    return tokens.next()


def factor( ):
    """factor = number |  variable | '(' expression ')' """
    
    tok = tokens.peek( )
    if syntaxDebug: print ("Factor: ", tok)
    if tok == "(":
        tokens.next()
        expr = addExpr()
        tokens.next()
        return expr
    if re.match(tokens.number, tokens.peek()):
        expr = Number(tok)
        tokens.next( )
        return expr
    elif re.match(tokens.string, tokens.peek()):
        expr = String(tok)
        tokens.next()
        return expr
    elif not tokens.check_key(tokens.peek()):
        expr = Variable(tok)
        tokens.next( )
        return expr
    
    error("Invalid operand")
    return


def orExpr( ):
    """ relationalExpr = addExpr [ relation addExpr ]"""
    
    tok = tokens.peek( )
    if syntaxDebug: print ("orExpr: ", tok)
    left = andExpr( )
    tok = tokens.peek( )
    while tok == 'or':
        op = tok
        tokens.next()
        right = orExpr( )
        left = BinaryExpr(op, left, right)
        tok = tokens.peek( )
    return left

def andExpr( ):
    """ relationalExpr = addExpr [ relation addExpr ]"""
    
    tok = tokens.peek( )
    if syntaxDebug: print ("andExpr: ", tok)
    left = relation( )
    tok = tokens.peek( )
    while tok == 'and':
        op = tok
        tokens.next()
        right = andExpr( )
        left = BinaryExpr(op, left, right)
        tok = tokens.peek( )
    return left

def relation( ):
    """ relationalExpr = addExpr [ relation addExpr ]"""
    
    tok = tokens.peek( )
    if syntaxDebug: print ("relation: ", tok)
    left = addExpr( )
    tok = tokens.peek( )
    while str(tok) in tokens.relational:
        op = tok
        tokens.next()
        
        right = relation()
        left = BinaryExpr(op, left, right)
        tok = tokens.peek()
    return left

def term( ):
    """ term    = factor { ('*' | '/') factor } """
    
    tok = tokens.peek( )
    if syntaxDebug: print ("Term: ", tok)
    left = factor( )
    tok = tokens.peek( )
    while tok == "*" or tok == "/":
        op = tok
        tokens.next()
        
        right = term( )
        left = BinaryExpr(op, left, right)
        tok = tokens.peek( )
    return left

def addExpr( ):
    """ addExpr    = term { ('+' | '-') term } """
    tok = tokens.peek( )
    if syntaxDebug: print ("addExpr: ", tok)
    
    left = term( )
    tok = tokens.peek( )
    while tok == "+" or tok == "-":
        op = tok
        tokens.next()
        
        right = addExpr( )
        left = BinaryExpr(op, left, right)
        tok = tokens.peek( )
    return left


def start( text ) :
    global tokens
    tokens = Lexer( text )
    stmtlist = parseStmtList( )
    if tokens.peek() != None:
        print(str(stmtlist))
        error("Not all input read")
    print (str(stmtlist))
    return


# Lexer, a private class that represents lists of tokens from a Gee
# statement. This class provides the following to its clients:
#
#   o A constructor that takes a string representing a statement
#       as its only parameter, and that initializes a sequence with
#       the tokens from that string.
#
#   o peek, a parameterless message that returns the next token
#       from a token sequence. This returns the token as a string.
#       If there are no more tokens in the sequence, this message
#       returns None.
#
#   o next, a parameterless message that advances to the next token
#       and returns that token.  At EOF, returns None.
#
#   o __str__, a parameterless message that returns a string representation
#       of a token sequence, so that token sequences can print nicely

class Lexer :
    
    
    # The constructor with some regular expressions that define Gee's lexical rules.
    # The constructor uses these expressions to split the input expression into
    # a list of substrings that match Gee tokens, and saves that list to be
    # doled out in response to future "peek" messages. The position in the
    # list at which to dole next is also saved for "nextToken" to use.
    keywords = keyword.kwlist
    #keywords.append('fi')
    special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"
    relational = "<=?|>=?|==?|!="
    arithmetic = "\+|\-|\*|/"
    #char = r"'."
    string = r"'[^']*'" + "|" +  r'"[^"]*"'
    number = r"\-?\d+(?:\.\d+)?"
    literal = string + "|" + number
    #idStart = r"a-zA-Z"
    #idChar = idStart + r"0-9"
    #identifier = "[" + idStart + "][" + idChar + "]*"
    identifier = "[a-zA-Z]\w*"
    lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier
    
    def __init__( self, text ) :
        self.tokens = re.findall( Lexer.lexRules, text )
        self.position = 0
        self.indent = [ 0 ]
    
    
    # The peek method. This just returns the token at the current position in the
    # list, or None if the current position is past the end of the list.
    
    
    def peek( self ) :

        if self.position < len(self.tokens) :
            return self.tokens[ self.position ]
        else :
            return None
    
    def check_key(self, object):
        
        return (object in self.keywords)
    
    # The removeToken method. All this has to do is increment the token sequence's
    # position counter.
    
    def next( self ) :
        self.position = self.position + 1
        
        return self.peek( )
    
    
    # An "__str__" method, so that token sequences print in a useful form.
    
    def __str__( self ) :
        return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"



def delComment(line):
    pos = line.find("#")
    if pos > -1:
        line = line[0:pos]
        line = line.rstrip()
    return line

def mklines(filename):
    inn = open(filename, "r")
    lines = [ ]
    pos = [0]
    ct = 0
    for line in inn:
        ct += 1
        line = line.rstrip( )
        line = delComment(line)
        if len(line) == 0: continue
        print (ct, "\t", line)
        lines.append(line)
    # print len(pos)
    return lines



def main():
    """main program for testing"""
    global debug
    filename = ""
    if sys.platform == "win32":
        filename = input("Filename? ")
    else:
        #filename = str(input("Filename? "))
        filename = sys.argv[1]
    start("".join(mklines(filename)))
    return


main()
