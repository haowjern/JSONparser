# learnt unit testing: https://docs.python-guide.org/writing/tests/

import ply.lex as lex
import ply.yacc as yacc
import sys

### CREATE LEXER
## TOKENS LIST
tokens = (
    "CONTROL_CHAR",
    "LBRACE",
    "RBRACE",
    "LSQBRACKET",
    "RSQBRACKET",
    "COLON",
    "COMMA",
    "QUOTATION",
    "BACKSLASH",
    "FLOAT",
    "INT",
    "TRUE",
    "FALSE",
    "NULL",
    "UNICODE_CHAR",
)


## LEXING RULES
def t_CONTROL_CHAR(t):
    r'(\\")|(\\\\)|(\\\/)|(\\b)|(\\f)|(\\n)|(\\r)|(\\t)|(\\u[0-9A-Fa-f]{4})'
    #print('control char:', t.value)
    return t

# def t_NUMBER(t):  # t is always a token
#     r'-?(0|([1-9][0-9]*))((\.[0-9])?)((e|E)(\+|-)?[0-9]*)?'
#     t.value = int(t.value)
#     return t

def t_LBRACE(t):
    r'{'
    return t

def t_RBRACE(t):
    r'}'
    return t

def t_LSQBRACKET(t):
    r'\['
    return t

def t_RSQBRACKET(t):
    r'\]'
    return t

def t_COLON(t):
    r':'
    return t

def t_COMMA(t):
    r','
    return t

def t_QUOTATION(t):
    r'"'
    return t

def t_BACKSLASH(t):
    r'\\'
    return t

def t_FLOAT(t):
    r'-?(0|[1-9][0-9]*)\.[0-9]+([eE][-+]?[0-9]+)?'
    return t

def t_INT(t): #add 0|[1-9][0-9]*
    r'-?(0|[1-9][0-9]*)([eE][-+]?[0-9]+)?'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_NULL(t):
    r'null'
    return t

# weird how unicode chars cannot be extended to multiple unicode chars
def t_UNICODE_CHAR(t): # r'[^\u005C^\u201C^\u201D]+' # not picking up a-z
    r'[\u0000-\uFFFD]'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Performing action (in this case, error)
def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = " \t\n"  # Spaces and tabs are ignored
## LEXING RULES end

#lexer = lex.lex() # Generate parser

# for testing purposes
def test_lexer(self, data):
    self.input(data)
    while True:
        tok = self.token()
        if not tok:
            break
        print(tok)

#test(lexer, test_wrong_obj)

### PARSER
# --- Parsing rules ---
def p_object(p):
    '''object : LBRACE members RBRACE
              | LBRACE empty RBRACE '''
    p[0] = p[2] # since p[2] always have the left and right braces
    #print("Object:", p[0])

def p_members(p):
    '''members : member COMMA members
               | member'''

    kv_dict = {}
    if len(p) == 4: # add nested dictionaries
        kv_dict.update(p[1])
        kv_dict.update(p[3])

        p[0] = kv_dict
    else:
        p[0] = p[1] # the only member in the object
    #print("members:", p[0])

def p_member(p):
    '''member : string COLON value'''
    kv_dict = {}
    if len(p) == 4: # member of a dict in the format K:V
        kv_dict[p[1]] = p[3]
        p[0] = kv_dict
    else:
        p[0] = p[1] # else empty dict
    #print("member:", p[0])

def p_string(p):
    '''string : QUOTATION characters QUOTATION'''
    p[0] = f"{p[2]}" # string must be "..."
    #print("String:", p[0])

def p_characters(p):
    '''characters : character characters
                  | character'''
    #print("Initial Characters: ", p[0])
    string = ""
    if p[1] is not None: # join one string character together into one string
        string += p[1]

    if len(p) == 3: # join next string character together into one string
        if p[2] is not None:
            string += p[2]
    p[0] = string
    #print("New Characters:", p[0])

def p_character(p):
    '''character : UNICODE_CHAR
                 | CONTROL_CHAR
                 | LBRACE
                 | RBRACE
                 | LSQBRACKET
                 | RSQBRACKET
                 | COLON
                 | COMMA
                 | FLOAT
                 | INT
                 | TRUE
                 | FALSE
                 | NULL
                 | empty'''
    p[0] = p[1] # avoided using sing BACKSLASH tokens and single QUOTATION tokens
    #print("Character:", p[0])

def p_number(p):
    '''number : FLOAT
              | INT'''
    if r'.' in p[1]: # if is a FLOAT token
        p[0] = float(p[1])
        #print(f'number float: {p[0]}')
    else:
        p[1] = float(p[1]) # for the case where there is an e as python treats numbers with e as a float
        p[0] = int(p[1])
        #print(f'number int: {p[0]}')

def p_array(p):
    '''array : LSQBRACKET valuelist RSQBRACKET'''
    p[0] = p[2] # valuelist is already a list type []
    #print("array:", p[0])

def p_valuelist(p):
    '''valuelist : valuelist COMMA value
                 | value
                 | empty'''
    vl_list = []
    if len(p) > 2: # append values into a list
        vl_list.append(p[1])
        vl_list.append(p[3])
        #p[0] = vl_list
    else:
        #p[0] = [p[1]]
        vl_list.append(p[1])
    p[0] = vl_list
    #print("valuelist:", p[0])

def p_value(p):
    '''value : string
             | number
             | object
             | array
             | TRUE
             | FALSE
             | NULL'''
    p[0] = p[1]
    #print("value:", p[0])

def p_empty(p):
    'empty :'
    pass

# Error rule
def p_error(p):
    #print(f"{p} Syntax error in input!")
    raise SyntaxError

# --- End parsing rules ---

def main():
    lexer = lex.lex()  # Generate parser
    parser = yacc.yacc() # create parser

    in_text = ""
    # If a filename has been specified, we parse it and report success/failure
    if len(sys.argv) == 2:
        file = open(sys.argv[1]).read()
        in_text = file

    # Otherwise, take input from the user
    else:
        while 1:
            line = input("Input text: ")
            if line:
                line += "\n"
                in_text += line
            else:
                break

    try:
        result = parser.parse(in_text)
    except SyntaxError:
        print("Error: input is not properly formatted JSON")
        sys.exit(0)
    print("Success: parsed input")


if __name__ == '__main__': main()






















