def getColumn(t):
  line_start = INPUT.rfind('\n', 0, t.lexpos) + 1
  return (t.lexpos-line_start)+1

# Tokens
#!Separacion de tipo de tokens(Mas orden)
#! AQUI SE DEFINE EL NOMBRE DEL TOKEN ##################################################
reserved = {
  'INICIO': 'reservada_inicio',
  'FIN': 'reservada_fin',
  'IF': 'reservada_if',
  'ELSE': 'reservada_else',
  'WHILE': 'reservada_while',
  'DO': 'reservada_do',
  'BREAK': 'reservada_break',
  'CONTINUE': 'reservada_continue', 
  'VOID': 'reservada_void',
  'RETUNR': 'reservada_return',
}


dato_boolean = {
  'TRUE': 'dato_boolean_true',
  'FALSE': 'dato_boolean_false',
}

signos_agrupacion = {
  '(': 'parentesis_abre',
  ')': 'parentesis_cierra',
  '{': 'llave_abre',
  '}': 'llave_cierra',
  '[': 'corchete_abre',
  ']': 'corchete_cierra',
}

signos_puntuacion = {
  ';': 'punto_coma',
  ',': 'coma',
  ':': 'dos_puntos',
  '.': 'punto',
}

tipo_de_datos = {
  'INT': 'tipo_int',
  'DOUBLE': 'tipo_double',
  'STRING': 'tipo_string',
  'CHAR': 'tipo_char',
  'BOOLEAN': 'tipo_boolean',
}


divicion = {
  '/': 'operador_divicion',
}
operadores = {
  '+': 'operador_suma',
  '-': 'operador_resta',
  '*': 'operador_multiplicacion',
  '%': 'operador_resto',
  '==': 'operador_igualacion',
  '!=': 'operador_diferenciacion',
  '>': 'operador_mayor',
  '>=': 'operador_mayor_igual',
  '<': 'operador_menor',
  '<=': 'operador_menor_igual',
  '&&': 'operador_AND',
  '||': 'operador_OR',
  '!': 'operador_NOT',
  '=': 'operador_igual',
}

tokens = (
  'comentario_unilinea',
  'comentario_multilinea',
  'dato_char',
  'dato_double',
  'dato_string',
  'numero',
  'id',
)  + tuple(tipo_de_datos.values()) + tuple(reserved.values()) + tuple(operadores.values()) + tuple(dato_boolean.values()) +tuple(signos_agrupacion.values())+tuple(signos_puntuacion.values())+tuple(divicion.values())


#! AQUI SE DEFINE EL TOKEN ##################################################
t_reservada_inicio = r'INICIO'
t_reservada_fin = r'FIN'

t_operador_suma = r'\+'
t_operador_resta = r'-'
t_operador_multiplicacion = r'\*'
t_operador_resto = r'%'
t_operador_igualacion = r'=='
t_operador_igual = r'='
t_operador_diferenciacion = r'!='
t_operador_mayor_igual = r'>='
t_operador_menor_igual = r'<='
t_operador_AND = r'&&'
t_operador_NOT = r'!'
t_operador_mayor = r'>'
t_operador_menor = r'<'
t_operador_OR = r'\|\|'


t_dato_boolean_true = r'TRUE'
t_dato_boolean_false = r'FALSE'
t_numero = r'\d+'

t_parentesis_abre = r'\('
t_parentesis_cierra = r'\)'
t_llave_abre = r'\{'
t_llave_cierra = r'\}'
t_corchete_abre = r'\['
t_corchete_cierra = r'\]'
t_punto_coma = r';'
t_coma = r','
t_dos_puntos = r':'
t_punto = r'\.'



t_tipo_int = r'INT'
t_tipo_double = r'DOUBLE'
t_tipo_string = r'STRING'
t_tipo_char = r'CHAR'
t_tipo_boolean = r'BOOLEAN'


t_operador_divicion = r'\/'

# Lexemas ignorados
t_ignore = ' \t\r\n'
"""
t:
- lineno: numero de linea
- value: valor del lexema
- type: nombre del token
"""
#! t_id BUSCA EN TOKEN tk_id NOMBRE DE FUNCION ##################################################
def t_id(t):                   #! <No debe de haber nada mas que esto
    r'[a-zA-Z_][a-zA-Z_0-9]*'  #! <No debe de haber nada mas que esto
    #! Si algo que no deberia ser idendentificador lo corrije 
    if t.value.upper() in reserved.keys(): 
        t.type = reserved[t.value.upper()]
    if t.value.upper() in tipo_de_datos.keys(): 
        t.type = tipo_de_datos[t.value.upper()]
    if t.value.upper() in dato_boolean.keys(): 
        t.type = dato_boolean[t.value.upper()]

    return t

def t_dato_double(t):                  
    r'\d+\.\d+' 
    return t
def t_dato_string(t):                  
    r'"[^"]*"' 
    return t
def t_dato_char(t):                  
    r'\'[^\']{1}\'' 
    return t
def t_comentario_unilinea(t):                  
    r'//[^\n]*\n' 
    return t
def t_comentario_multilinea(t):                  
    r'/\*[^*/]*\*/' 
    return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno+=len(t.value)
def t_error(t):
  print(t.lineno, getColumn(t), f"No se pudo reconocer el lexema '{t.value}'")
  t.lexer.skip(1)
  #!Presedemcia(mas arriba importan menos )
precedence = (
  ('left','operador_suma','operador_resta'),
  ('left','operador_multiplicacion','operador_resto')
)
"""
ASOCIATIVIDAD IZQUIERDA (left)
((5 + 5) + 5)
((5 ^ 5) ^ 5)
ASOCIATIVIDAD DERECHA (right)
(5 + (5 + 5))
(5 ^ (5 ^ 5))
"""
#! importante
"""
p[0] : Lado izquierdo de la producción
p[1+] : Lado derecho de la producción
Lo que habrá en los elementos del lado derecho será:
- Un token si es un símbolo terminal
- Lo que regresemos de su producción si es un símbolo no terminal
Para retornar algo de una producción se debe asignar a p[0]
"""
# Producciones
#! Aqui se definen producciones
def p_INITIAL(p):
  '''
  INITIAL : reservada_inicio EXPRESSIONS reservada_fin

  '''

  p[0] = p[2]
    #! Siempre asignarle algo al P[0]

#! Complicado 28:20
def p_EXPRESSIONS(p):
   
  '''
  EXPRESSIONS : EXPRESSIONS E
              | E
  '''
    
  if len(p)==3:
    
    p[0] = p[1]
    p[0].append(p[2])
  else:
    
    p[0] = [p[1]]
def p_E(p):
  '''
  E : E operador_suma E
    | E operador_resta E
    | E operador_multiplicacion E
    | E operador_divicion E
    | E operador_resto E
    | id
    | numero
  '''
  if len(p)==2:
    p[0] = {"linea": p.lexer.lineno, "columna": getColumn(p.lexer), "valor": p[1]}
  else:
    p[0] = {"linea": p.lexer.lineno, "columna": getColumn(p.lexer), "operacion": p[2], "izquierda": p[1], "derecha": p[3]}
def p_error(p):
  if p:
    print(f"Sintaxis no válida cerca de '{p.value}' ({p.type})")
  else:
    print("Ninguna instrucción válida")
from ply.yacc import yacc
from ply.lex import lex

lexer = lex()
parser = yacc()
#lexer.lex(reflags=re.IGNORECASE)  # case insensitive

INPUT = r'''
INICIO
9/2
FIN


    '''

ast = parser.parse(INPUT, lexer)

import json
print(json.dumps(ast, indent=10, sort_keys=False))

"""#! impresion de tokens
lexer.input(INPUT)
for tok in lexer:
    print(tok)"""
    



