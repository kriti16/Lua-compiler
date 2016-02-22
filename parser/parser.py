from lexer import Lualexer
import ply.yacc as yacc

class LuaParser(object):
    lexer = Lualexer().lexer
    def p_chunk_start(p):
        'chunk : chunk stat| empty '
        p[0] = p[1]
        
    def p_expression_plus(p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]

    def p_expression_minus(p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]

    def p_expression_term(p):
        'expression : term'
        p[0] = p[1]

    def p_term_times(p):
        'term : term TIMES factor'
        p[0] = p[1] * p[3]

    def p_term_div(p):
        'term : term DIVIDE factor'
        p[0] = p[1] / p[3]

    def p_term_factor(p):
        'term : factor'
        p[0] = p[1]

    def p_factor_num(p):
        'factor : NUMBER'
        p[0] = p[1]

    def p_factor_expr(p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]
    def p_empty(p):
        'empty :'
        pass
    
    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!")

    self.parser = yacc.yacc()
if __name__ == '__main__':
    parser = LuaParser().parser
