from ply.yacc import yacc
import json
from ply.lex import lex
from reporte_tokens import clase_token
import graphviz


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
) + tuple(tipo_de_datos.values()) + tuple(reserved.values()) + tuple(operadores.values()) + tuple(dato_boolean.values()) + tuple(signos_agrupacion.values())+tuple(signos_puntuacion.values())+tuple(divicion.values())


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


def t_id(t):  # ! <No debe de haber nada mas que esto
    r'[a-zA-Z_][a-zA-Z_0-9]*'  # ! <No debe de haber nada mas que esto
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
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(t.lineno, getColumn(t),
          f"No se pudo reconocer el lexema '{t.value}'")
    t.lexer.skip(1)


    #!Presedemcia(mas arriba importan menos )
precedence = (
    ('left', 'operador_OR'),
    ('left', 'operador_AND'),
    ('left', 'operador_igualacion', 'operador_diferenciacion'),
    ('left', 'operador_menor', 'operador_menor_igual','operador_mayor', 'operador_mayor_igual'),
    ('left', 'operador_suma', 'operador_resta'),
    ('left', 'operador_multiplicacion', 'operador_resto'),
    ('right', 'operador_NOT')
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
"""def p_sintactico(p):
  '''
  SINTACTICO : IF

               
  '''
  p[0] = p[1]

def p_IF(p):
  '''
  IF : reservada_if OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO
  '''
  p[0] = p[1]

def p_OPERACION(p):
  '''
  IF : reservada_if OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO
  '''
  p[0] = p[1]


"""


def p_S0(p):
    '''
      S0 : INITIAL
    '''
    print(p[1], "arroba")
def p_INITIAL_RECURSIVO(p):
    '''
    INITIAL : INITIAL ESTRUCTURA
    '''
    p[1].append(p[2]) #! nose xd
    p[0] = p[1] 
def p_INITIAL_INICIAL(p):
    '''
    INITIAL : ESTRUCTURA
    '''
    p[0] = [p[1]]

def p_ESTRUCTURA(p):
    '''
    ESTRUCTURA : PRODIF_ELSE
               | PRODIF
               | PRODDO_WHILE
               | PRODWHILE
               | PRODVOID
               | PRODFUNCION
                 
    '''
    p[0] = p[1]

def p_ESTRUCTURA_PRODDO_WHILE(p):
    '''
    PRODDO_WHILE : reservada_do INSTRUCCIONES_FACTORIZADO reservada_while OPERACION_FACTORIZADO punto_coma
    '''
    p[0] = p[0]

def p_ESTRUCTURA_PRODWHILE(p):
    '''
    PRODWHILE : reservada_while OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO 
    '''
    p[0] = p[0]

def p_ESTRUCTURA_IF_ELSE(p):
    '''
    PRODIF_ELSE : reservada_if OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO reservada_else INSTRUCCIONES_FACTORIZADO
    '''
    p[0] = p[1]

def p_ESTRUCTURA_IF(p):
    '''
    PRODIF : reservada_if OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO
    '''
    p[0] = p[1]

def p_ESTRUCTURA_VOID(p):
    '''
    PRODVOID : reservada_void id PARAMETROS_FACTORIZADO INSTRUCCIONES_FACTORIZADO
    '''
    p[0] = p[1]

def p_ESTRUCTURA_FUNCION(p):
    '''
    PRODFUNCION : TIPO_DATO id PARAMETROS_FACTORIZADO INSTRUCCIONES_FACTORIZADO
    '''
    p[0] = p[1]


def p_OPERACION(p):
    '''
    OPERACION : OPERACION operador_suma OPERACION
            |   OPERACION operador_resta OPERACION
            |   OPERACION operador_multiplicacion OPERACION
            |   OPERACION operador_divicion OPERACION
            |   OPERACION operador_resto OPERACION
            |   OPERACION operador_igualacion OPERACION
            |   OPERACION operador_diferenciacion OPERACION
            |   OPERACION operador_mayor OPERACION
            |   OPERACION operador_mayor_igual OPERACION
            |   OPERACION operador_menor OPERACION
            |   OPERACION operador_menor_igual OPERACION
            |   OPERACION operador_AND OPERACION
            |   OPERACION operador_OR OPERACION
            |   OPERACION operador_NOT OPERACION
            |   OPERACION operador_igual OPERACION
            |   numero
    '''
def p_INSTRUCCIONES(p):
    '''
    INSTRUCCIONES : DECLARACION
                  | ASINGACION
                  | PRODIF_ELSE
                  | PRODIF
                  | PRODDO_WHILE
                  | PRODWHILE
                  | PRODVOID
                  | RETURN
                  | BREAK
                  | CONTINUE
                  | LLAMADA
                  
    '''
    p[0] = p[1]
#! AGREGAR TODO (FALTA)
def p_DECLARACIONES(p):
    '''
    DECLARACION : TIPO_DATO id operador_igual DATO punto_coma
    '''
    p[0] = p[1]
def p_ASIGNACION(p):
    '''
    ASINGACION : id operador_igual DATO punto_coma
    '''
    p[0] = p[1]
def p_TIPO_DATO(p):
  '''
  TIPO_DATO : tipo_int 
            | tipo_double
            | tipo_string
            | tipo_char
            | tipo_boolean
  
  '''
  
  p[0] = p[1]
def p_DATO(p):
  '''
  DATO : numero 
          | dato_double
          | dato_string
          | dato_char
          | dato_boolean_true
          | dato_boolean_false
  '''

  p[0] = p[1]
def p_PARAMETRO_DEFINICION(p):
    '''
    PARAMETRO : TIPO_DATO id
    '''
    p[0] = p[1]
def p_PARAMETROS_RECURSIVO(p):
    '''
    PARAMETROS :  PARAMETROS coma PARAMETRO 
               | PARAMETRO
               | 
    '''
    p[0] = p[1]
def p_LLAMADA(p):
    '''
    LLAMADA : id parentesis_abre ARGUMENTOS parentesis_cierra
    '''
    p[0] = p[1]
def p_ARGUMENTOS(p):
    '''
    ARGUMENTOS :  ARGUMENTOS coma ARGUMENTO 
               | ARGUMENTO
               | 
    '''
    p[0] = p[1]
def p_ARGUMENTO(p):
    ''' 
    ARGUMENTO :  DATO
    '''
    p[0] = p[1]

def p_RETURN(p):
    '''
    RETURN : reservada_return punto_coma 
           | reservada_return DATO punto_coma 
    '''
    p[0] = p[1]
def p_BREAK(p):
    '''
    BREAK : reservada_break punto_coma 
    '''
    p[0] = p[1]
def p_CONTINUE(p):
    '''
    CONTINUE : reservada_continue punto_coma 
    '''
    p[0] = p[1]


def p_FACTORIZACION_OPERACION(p):
    '''
    OPERACION_FACTORIZADO : parentesis_abre OPERACION parentesis_cierra
    '''
    p[0] = p[1]
def p_FACTORIZACION_INSTRUCCIONES(p):
    '''
    INSTRUCCIONES_FACTORIZADO : llave_abre INSTRUCCIONES llave_cierra
    '''
    p[0] = p[1]
def p_FACTORIZACION_PARAMETROS(p):
    '''
    PARAMETROS_FACTORIZADO : parentesis_abre PARAMETROS parentesis_cierra
    '''
    p[0] = p[1]








#!  28:20
"""
def p_EXPRESSIONS(p):
    '''
    EXPRESSIONS : EXPRESSIONS E
    '''
    p[0] = p[2]


def p_EXPRESSIONS_VALOR(p):
    '''
    EXPRESSIONS : E
    '''
    p[0] = p[1]


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

    if len(p) == 2:
        p[0] = {"linea": p.lexer.lineno,
                "columna": getColumn(p.lexer), "valor": p[1]}
    else:
        p[0] = {"linea": p.lexer.lineno, "columna": getColumn(
            p.lexer), "operacion": p[2], "izquierda": p[1], "derecha": p[3]}

    p[0] = "@"







"""


def p_error(p):
    if p:
        print(f"Sintaxis no válida cerca de '{p.value}' ({p.type})")
    else:
        print("Ninguna instrucción válida")


lexer = lex()
parser = yacc()
# lexer.lex(reflags=re.IGNORECASE)  # case insensitive

INPUT = r'''
if (5*5) {int a = "s";} else {int a = 55 ;}

if (1*1) {int a = 1;} else {int a = 1;}
'''

ast = parser.parse(INPUT, lexer)

print(json.dumps(ast, indent=10, sort_keys=False))


"""while (5*5) {int a = 55 ;}
do {int a = 55 ;} while (5*5) ;
void a (int a) {string a = "55";}
void a (int a) {int a = 55;}"""


#! ARBOL SINTACTICO
def graficar(self):
    inicio = """digraph html {"""
    final ="""}"""
 
    medio = self.pedidos.imprimir()

    documento = inicio + medio + final
    g = Source(documento, filename="gola" +'_copia.gv',format="png")
    g.view()

def imprimir(self):
    puntero= self.end
    dato_pizza=""
    while puntero != None:
        print(puntero.dato)
            
        dato_pizza= dato_pizza + "Q"+str(id(puntero.dato))+"[label=\""+puntero.dato.string()+"\"]\n"
        if puntero.anterior != None:
            dato_pizza=dato_pizza+"Q"+str(id(puntero.dato)) +"->"+"Q"+str(id(puntero.anterior.dato))+"\n"

        puntero = puntero.anterior

    return dato_pizza


















#! impresion de tokens
lista_tokens=[]
lexer.input(INPUT)
linea=0
iteracion=0
for tok in lexer:
    iteracion=iteracion+1
    columna=getColumn(tok)
    if columna == 1:
        linea = linea +1
    lista_tokens.append(clase_token(linea,columna,tok.value,tok.type,iteracion))
    
inicio="<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"estilo.css\"/></head><body>"
cuerpo = "<table class=\"styled-table\"><tr class=\"active-row\"><th>LINEA</th><th>COLUMNA</th><th>LEXEMA</th><th>TIPO</th></tr><tbody>"
concatenar = ""
for element in lista_tokens:
    concatenar = concatenar + element.html()
cuerpo_token="<h1>REPORTE DE TOKENS</h1>"+ cuerpo +concatenar+ "</tbody></table>"
final = inicio +cuerpo_token+"</html></body>"
#input("introdusca el nombre del reporte HTML :")
f = open ("si"+".html",'w')
f.write(final)
f.close()


