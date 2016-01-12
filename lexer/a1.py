import ply.lex as lex
import numpy as np
from collections import defaultdict
keywords =  ('and', 'break', 'do', 'else', 'elseif',
	'end', 'false', 'for', 'function', 'goto', 'if',
	'in', 'local', 'nil', 'not', 'or', 'repeat',
	'return', 'then', 'true', 'until', 'while')

operators= (
     'EQUALS','PLUS','MINUS','TIMES','DIVIDE','POWER',
     'LPAREN','RPAREN','LT','LE','GT','GE','NE',
     'COMMA','SEMI', 'INTEGER','FLOAT', 'STRING','COLON',
     'ID','NEWLINE','CHECKEQ','HASH','SDOT','TDASH',
    'RCURLY','LCURLY','LSQUARE','RSQUARE','COMMENT','MODULO'
)

t_ignore = ' \t'

tokens = keywords + operators

def t_ID(t):
    r'[A-Za-z][A-Z0-9a-z\_]*'
    if t.value in keywords:
        t.type = t.value
    return t
    
t_EQUALS  = r'=' #assignment equal
t_CHECKEQ = r'==' #Check equality
t_HASH = r'\#'
t_PLUS    = r'\+' #addition
t_MINUS   = r'-' #difference
t_TIMES   = r'\*' #product
t_POWER   = r'\^' #power
t_DIVIDE  = r'/' #divide
t_SDOT = r'\.' #Single Dot
t_MODULO =r'%' #Modulo
t_TDASH = r'---' #Triple Dot
t_COLON = r':' #Colon
t_COMMENT = r'--(.*)'
t_LPAREN  = r'\(' #left parenthesis
t_RPAREN  = r'\)' #right parenthesis
t_RCURLY = r'{'
t_LCURLY = r'}'
t_LSQUARE = r'\['
t_RSQUARE = r']'
t_LT      = r'<' #less than
t_LE      = r'<=' #less than equal
t_GT      = r'>' #greater than
t_GE      = r'>=' #greter than equal
t_NE      = r'~=' #not equal 
t_COMMA   = r'\,' #comma
t_SEMI    = r';' #semicolon
t_INTEGER = r'\d+'    #integer 
t_FLOAT   = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))' #float
t_STRING  = r'(\".*?\")|(\'.*?\')'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print "Illegal character", t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

#Create an empty Dictionary
class stru:
    def __init__(self):
        self.frequency = 0
        self.listOfOccurences = []

D = defaultdict(stru)
#D = {k:0 for k in tokens}

#Get the file name
fname = raw_input("Give File name>  ")


#Read the File
f = open(fname,'r')
data = f.read()
f.close()

lexer.input(data)

# Tokenize

while True:
    tok = lexer.token()
    #Get the  end
    if not tok or tok == None: 
        break    
    #print tok
    #print tok.value,tok.type   ##Uncomment this to print each token
    if tok.type == 'ID' or tok.type == 'INTEGER' or tok.type == 'STRING' or tok.type == 'FLOAT' or len(D[tok.type].listOfOccurences) == 0:
        D[tok.type].listOfOccurences.append(tok.value)
    D[tok.type].frequency = D[tok.type].frequency + 1

for k in D.keys():
        print k,D[k].frequency,D[k].listOfOccurences
