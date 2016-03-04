from __future__ import print_function
from lexer import Lualexer
import ply.yacc as yacc
import sys
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()
class node(object):
	def __init__(self, value, children = []):
		self.value = value
		self.children = children


proto = type(node(5))

class LuaParser(object):

    def __init__(self):
        lexerClass = Lualexer()
        lexer = lexerClass.lexer
        tokens = lexerClass.tokenList

        def p_sdash_start(p):
        	'''sdash : chunk
        	| chunk laststat
        	| chunk laststat SEMI'''
        	p[0] = node ("SCHUNK",p[1:])
    
        def p_chunk(p):
            '''chunk : chunk stat
            | chunk stat SEMI
    	    | stat SEMI
            | stat
            '''
            p[0] = node ("CHUNK",p[1:])
            
        def p_block_chunk(p):
            ''' block : sdash'''
            p[0] = node ("BLOCK",p[1:])
            
        def p_stat_statement(p):
            '''stat :  varlist EQUALS explist  
            | do block end
            | functioncall
            | while exp do block end 
	    | repeat block until exp 
	    | if exp then block ifblock else block end 
            | if exp then block ifblock  end 
	    | for names EQUALS exp COMMA exp  do block end 
            | for names EQUALS exp COMMA exp COMMA exp do block end 
	    | for namelist in explist do block end 
	    | local namelist 
            | local namelist EQUALS explist
            | function funcname funcbody
            | local function names funcbody'''
            p[0] = node ("STAT",p[1:])

        def p_funcbody_parlist(p):
            '''funcbody : LPAREN RPAREN block end
            | LPAREN  parlist RPAREN block end'''
            p[0] = node ("FUNCBODY",p[1:])

        def p_functioncall_prefix(p):
            '''functioncall : prefixexp args'''
            p[0] = node ("FUNC_CALL",p[1:])


        def p_args_explist(p):
            '''args : LPAREN RPAREN
            | LPAREN explist RPAREN
            | tableconstructor
            | STRING'''
            p[0] = node ("ARGS",p[1:])

        def p_parlist_namelist(p):
            '''parlist : namelist 
            |  namelist comtrp  %prec comtrp
            | TRPLDOTS'''
            p[0] = node ("PARLIST",p[1:])

        def p_comtrp_parlist(p):
            'comtrp : COMMA TRPLDOTS'
            p[0] = node ("COMTRP",p[1:])

        def p_laststat_break(p):
            '''laststat : return retexplist 
            | return 
            | break'''
            p[0] = node ("LASTSTAT",p[1:])

        def p_funcname_names(p):
            '''funcname : names dotid COLON 
            | names'''
            p[0] = node ("FUNCNAME",p[1:])

        def p_dotid(p):
            '''dotid : SDOT names dotid 
            | empty'''
            p[0] = node ("DOTIT",p[1:])

        def p_comvar(p):
            '''comvar : COMMA var comvar 
            | empty'''
            p[0] = node ("COMVAR",p[1:])

        def p_comid(p):
            '''comid : COMMA names comid 
            | empty'''
            p[0] = node ("COMID",p[1:])
            
        def p_ifblock_elseif(p):
            '''ifblock : ifblock elseif exp then block 
            | empty '''
            p[0] = node ("IFBLOCK",p[1:])
        
        def p_varlist_var(p):
            '''varlist : var comvar '''
            p[0] = node ("VARLIST",p[1:])

        def p_var_names(p):
            '''var :  names 
            | prefixexp LSQUARE exp RSQUARE 
            | prefixexp SDOT names '''
            p[0] = node ("VARNAMES",p[1:])

        def p_namelist_names(p):
            'namelist :  names  comid'
            p[0] = node ("NAMELIST",p[1:])

        def p_explist_exp(p):
            '''explist : explist COMMA exp
            | exp '''
            p[0] = node ("EXPLIST",p[1:])


        def p_exp_oper(p):
            '''exp :  nil 
            | false 
            | true 
            | Number 
            | STRING 
            | TRPLDOTS 
            | function 
	    | prefixexp 
            | exp PLUS exp
            | exp MINUS exp
            | exp TIMES exp
            | exp DIVIDE exp
            | exp POWER exp
            | exp LT exp
            | exp LE exp
            | exp GT exp
            | exp GE exp
            | exp NE exp
            | exp CHECKEQ exp
            | exp and exp
            | exp or exp
            | exp MODULO exp
            | exp DBLDOTS exp
            | tableconstructor
            | unop exp  %prec unop'''
	    p[0] = node ("EXP",p[1:])


        def p_retexplist_exp(p):
            '''retexplist : retexplist COMMA retexp
            | retexp '''
            p[0] = node ("RETEXPLIST",p[1:])


        def p_retexp_oper(p):
            '''retexp :  nil 
            | false 
            | true 
            | Number 
            | STRING 
            | TRPLDOTS 
            | prefixexp 
            | exp PLUS exp
            | exp MINUS exp
            | exp TIMES exp
            | exp DIVIDE exp
            | exp POWER exp
            | exp LT exp
            | exp LE exp
            | exp GT exp
            | exp GE exp
            | exp NE exp
            | exp CHECKEQ exp
            | exp and exp
            | exp or exp
            | exp MODULO exp
            | exp DBLDOTS exp
            | tableconstructor
	    | unop exp  %prec unop'''
	    p[0] = node ("RETEXP",p[1:])


            
        def p_Number_ints(p):
            '''Number : INTEGER 
            | FLOAT 
            | HEX '''
            p[0] = node ("NUMBER",p[1:])
        
        def p_empty(p):
            'empty : '
            pass


        def p_prefixexp_exp(p):
            ''' prefixexp : var 
            |  LPAREN exp RPAREN 
            | functioncall'''
            p[0] = node ("PREFIXEXP",p[1:])

        def p_unop_ops(p):
            '''unop : MINUS
            | not
            | HASH'''
            p[0] = node ("UNOP",p[1:])
            # Error rule for syntax errors

        def p_tableconstructor_fieldlist(p):
            '''tableconstructor : LCURLY fieldlist RCURLY 
            | LCURLY RCURLY'''
            p[0] = node ("TABLECONSTRUCTOR",p[1:])

        def p_fieldlist_fieldseplist(p):
            '''fieldlist : field fieldseplist fieldsep
            | field fieldseplist'''
            p[0] = node ("FIELDLIST",p[1:])
            
        def p_fieldseplist_field(p):
            ''' fieldseplist : fieldseplist fieldsep field 
            | empty'''
            p[0] = node ("FIELDSEPLIST",p[1:])

        def p_field_exp(p):
            '''field : LSQUARE exp RSQUARE EQUALS exp 
            | names EQUALS exp 
            | exp'''
            p[0] = node ("FIELD",p[1:])

        def p_fieldsep_seps(p):
          '''fieldsep : COMMA 
          | SEMI'''
          p[0] = node ("FIELDSEP",p[1:])

        def p_error(p):
            print("Syntax error in input!")

        def p_names_id(p):
            '''names : ID
            | RESID'''
            p[0] = node ("NAMES",p[1:])

        precedence = (
            ('nonassoc','comtrp'),
            ('left','LPAREN'),
            ('right','RPAREN'),
            ('right','COMMA'),
            ('left','LT','GT','LE','GE','NE','CHECKEQ','and','or'),
            ('right','DBLDOTS'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'TIMES', 'DIVIDE','MODULO'),
            ('right', 'unop'),  #uminus left to handle
            ('right', 'POWER')
        )

        self.parser = yacc.yacc(debug=True,debuglog=log,start='sdash')
#        self.parser = yacc.yacc(start='sdash')


def print_right_most(start):
	der = [start]
	done = 0
	print("<p> <font color=\"red\"> START </font> </p>")
	while not done:
	    right = -1;
	    for i in range(len(der)):
		if type(der[i]) == proto:
		    right = i	
	    print ("<p>" , end = " ")
	    for i in range(len(der)):
		if type(der[i]) == proto:
		    if i == right:
			print("<font color=\"red\">", end = " ")
			print(der[i].value,end=" ")
			print("</font> ", end = " ")
		    else:
			print(der[i].value,end=" ")
		else:
		    print(der[i],end=" ")
			
			
	    print("</p>")
	    if right!=-1:
		der = der[:right] + der[right].children + der[right+1:]
	    else:
		done = 1

			

fname=sys.argv[1]
f = open(fname,'r')
data = f.read()
f.close()



# Set up a logging object

# parser.parse(input,debug=log)

# yacc.yacc(debug=True,debuglog=log)

if __name__ == '__main__':
    parser = LuaParser().parser      
    result = parser.parse(data,debug=log)
#    result = parser.parse(data)
    print_right_most(result)
