from lexer import Lualexer
import ply.yacc as yacc

class LuaParser(object):

    def __init__(self):
        lexerClass = Lualexer()
        lexer = lexerClass.lexer
        tokens = lexerClass.tokenList

        def p_sdash_start(p):
        	'''sdash : chunk
        	| chunk laststat
        	| chunk laststat SEMI'''
    
        def p_chunk(p):
            '''chunk : chunk stat
            | chunk stat SEMI
            | empty'''
            p[0] = p[1]
            
        def p_block_chunk(p):
            ''' block : chunk'''
            p[0] = p[1]
            
        def p_stat_statement(p):
            '''stat :  varlist EQUALS explist  
            | do block end 
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

        def p_funcbody_parlist(p):
            '''funcbody : LPAREN  RPAREN block end
            | LPAREN  parlist RPAREN block end'''


        def p_parlist_namelist(p):
            '''parlist : namelist 
            |  namelist comtrp  %prec comtrp
            | TRPLDOTS'''

        def p_comtrp_parlist(p):
            'comtrp : COMMA TRPLDOTS'

        def p_laststat_break(p):
            '''laststat : return explist 
            | return 
            | break'''
        def p_funcname_names(p):
            '''funcname : names dotid COLON 
            | names dotid '''
        def p_dotid(p):
            '''dotid : SDOT names dotid 
            | empty'''
        def p_comvar(p):
            '''comvar : COMMA var comvar 
            | empty'''

        def p_comid(p):
            '''comid : COMMA names comid 
            | empty'''
            
        def p_ifblock_elseif(p):
            '''ifblock : ifblock elseif exp then block 
            | empty '''
            p[0] = p[1]
        
        def p_varlist_var(p):
            '''varlist : var comvar '''

        def p_var_names(p):
            '''var :  names 
            | prefixexp LSQUARE exp RSQUARE 
            | prefixexp SDOT names '''

        def p_namelist_names(p):
            'namelist :  names comid'

        def p_explist_exp(p):
            '''explist : explist COMMA exp
            | exp '''

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
            | unop exp  %prec unop
            | tableconstructor'''

        def p_Number_ints(p):
            '''Number : INTEGER 
            | FLOAT 
            | HEX '''
        
        def p_empty(p):
            'empty :'
            pass

        def p_prefixexp_exp(p):
            ''' prefixexp : var 
            |  LPAREN exp RPAREN '''

        def p_unop_ops(p):
            '''unop : MINUS
            | not
            | HASH'''
            # Error rule for syntax errors

        def p_tableconstructor_fieldlist(p):
            '''tableconstructor : LCURLY fieldlist RCURLY 
            | LCURLY RCURLY'''

        def p_fieldlist_fieldseplist(p):
            '''fieldlist : field fieldseplist fieldsep
            | field fieldseplist'''
            
        def p_fieldseplist_field(p):
            ''' fieldseplist : fieldseplist fieldsep field 
            | empty'''

        def p_field_exp(p):
            '''field : LSQUARE exp RSQUARE EQUALS exp 
            | names EQUALS exp 
            | exp'''

        def p_fieldsep_seps(p):
            '''fieldsep : COMMA 
            | SEMI'''

        def p_error(p):
            print("Syntax error in input!")

        def p_names_id(p):
            '''names : ID
            | RESID'''

        precedence = (
            ('nonassoc','comtrp'),
            ('nonassoc','COMMA'),
            ('left','LT','GT','LE','GE','NE','CHECKEQ','and','or'),
            ('right','DBLDOTS'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'TIMES', 'DIVIDE','MODULO'),
            ('right', 'unop'),  #uminus left to handle
            ('right', 'POWER')
        )

        self.parser = yacc.yacc()

if __name__ == '__main__':
    parser = LuaParser().parser
    while True:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
