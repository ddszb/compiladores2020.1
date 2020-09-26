# ------------------------------------------------------------
# Processing a log file
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'TIMESTAMP',
    'PROC',
    'MESSAGE'
]

t_ignore = '\n'

def t_TIMESTAMP(t):
    r'\d\d:\d\d:\d\d\.\d\d\d\d\d\d\s-\d\d\d\d'
    t.type ='TIMESTAMP'
    return t

def t_PROC(t):
    r'\t[a-zA-Z]+\t'
    t.value = t.value[1:len(t.value) - 1]
    return t

def t_MESSAGE(t):
    r'.+\n([^\d\n]\s*.*\n?)*'
    t.value = t.value[:len(t.value) - 1]
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


class LogProcLexer:
    data = None
    lexer = None
    def __init__(self):
        fh = open("log", 'r')
        self.data = fh.read()
        fh.close()
        self.lexer = lex.lex()
        self.lexer.input(self.data)

    def collect_messages(self):
        expected_process = 'kernel'
        proc_type = 'PROC'
        tokens = []
        while True:
                tok = self.lexer.token()
                # Tratando eof
                if not tok:
                    break
                if tok.type == proc_type and tok.value == expected_process:
                    tokens.append(self.lexer.token())
        return tokens


if __name__ == '__main__':
    print(LogProcLexer().collect_messages())
    
