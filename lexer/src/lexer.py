import ply.lex as lex
import numpy as np
import sys
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
    'RCURLY','LCURLY','LSQUARE','RSQUARE','MODULO','HEX','RESID','DBLDOTS', 'TRPLDOTS'
)

t_ignore = ' \t \n'

tokens = keywords + operators
def t_RESID(t):
    r'_[A-Z\_]+'
    return t    #Reserved Identifiers

def t_ID(t):
    r'[A-Za-z\_][a-z\_]*[A-Z0-9a-z\_]*'
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
t_DBLDOTS = r'\.\.' #concatenation
t_TRPLDOTS = r'\.\.\.' 
t_ignore_COMMENT  = r'--(.*)'
t_ignore_MULTCOMMENT = r'--\[\[ [^-]*[^-]*[^\]]*[^\]]* --\]\]'
#r'--\[\[  [^(--\]\])]* --\]\]'
#r'--\[\[  (. | \n)* --\]\]'
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
t_INTEGER = r'\d+([eE]\d+)?'    #integer 
#t_FLOAT   = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+)|([1-9]\d*e[\+-]?\d+))' #float
t_FLOAT   = r'((\d+\.\d+E[\+-]?\d+) | (\d+\.\d+e[\+-]?\d+) | \d+\.\d+)' #float
t_STRING  = r'(\".*?\")|(\'.*?\')'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print t.value[0]
    raise ValueError('Illegal Character ')
    t.lexer.skip(1)

def t_HEX(t):
    r'0[xX][0-9a-fA-F]+( ([pP][\+-]?\d+) | (\.[0-9a-fA-F]+([pP][\+-]?\d+)?) )?'
    #t.value = int(t.value,0)
    return t
lexer = lex.lex()

#Create a class to keep frequency and list of lexemes
class stru:
    def __init__(self):
        self.frequency = 0
        self.listOfOccurences = []

D = defaultdict(stru)
#Get the file name
#fname = raw_input("Give File name>  ")
#fname = "big.lua"
fname=sys.argv[1]
#Read the File
#print fname
f = open(fname,'r')

data = f.read()
#print data
f.close()

lexer.input(data)

# Tokenize

while True:
    tok = lexer.token()
    if not tok or tok == None: 
        break    
    if tok.type == 'ID' or tok.type == 'INTEGER' or tok.type == 'STRING' or tok.type == 'FLOAT' or tok.type == 'HEX' or len(D[tok.type].listOfOccurences) == 0:
        if tok.type == 'STRING':
            tok.value = tok.value.strip('"')
        D[tok.type].listOfOccurences.append(tok.value)
#        print D[tok.type].listOfOccurences
    print tok
    
    D[tok.type].frequency = D[tok.type].frequency + 1

for k in D.keys():
        print k+"\t"+str(D[k].frequency)+"->"+str(D[k].listOfOccurences)