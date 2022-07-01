import graphviz
from numpy import flexible
from ply.yacc import yacc
import json
from ply.lex import lex
from reporte_tokens import clase_token
from graphviz import Source

class nodo:

    def __init__(self,nombre ):
        self.hijos = []
        self.nombre = nombre

    def agregar_hijo(self,hijo):
        self.hijos.append(hijo)


    def graficar(self):
        concatenar = ""
        
        for hijo in self.hijos:
            print(hijo)
            if( type(hijo)!= nodo):
                concatenar = concatenar +  "q"+str(id(hijo))+"[label=\""+str(hijo)+"\"]\n"
            else:
                concatenar = concatenar + hijo.graficar()
            flecha = "q"+str(id(self ))+" -> "+ "q"+str(id(hijo)) + "\n"
            concatenar = concatenar + flecha 

        valor_propio = "q"+str(id(self))+"[label=\""+str(self.nombre)+"\"]\n"

        concatenar = concatenar + valor_propio
        return concatenar

        


def getColumn(t):
    line_start = INPUT.rfind('\n', 0, t.lexpos) + 1
    return (t.lexpos-line_start)+1
    
def digraph(string):
    
    inicio = 'digraph html {'
    final ='}'

    documento = inicio + string  + final
    #input("introdusca el nombre del reporte HTML :")
    g = Source(documento, filename=input("introdusca el nombre del arbol sintactico : "),format="pdf")
    g.view()

def label(a):
    label_arbol=[]
    x=0
    for hoja in a :
        if type(hoja) == list:
            hijo(hoja,label_arbol)
        else:
            label_arbol.append("Q"+str(id(a[x]))+"[label=\""+str(hoja)+"\"]\n")
            x=x+1
    return label_arbol

def hijo(lista,otra_lista):
    x=0
    for hoja in lista :
        if type(hoja) == list:
            hijo(hoja,otra_lista)
        else:
            otra_lista.append("Q"+str(id(lista[x]))+"[label=\""+str(hoja)+"\"]\n")
            x=x+1
    return otra_lista


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

# Producciones


def p_S0(p):
    '''
      S0 : INITIAL
    '''
    p[0] = nodo("S0")
    p[0].agregar_hijo(p[1])

    string=p[0].graficar()
    digraph(string)
    

    #print(p[1])
def p_INITIAL_RECURSIVO(p):
    '''
    INITIAL : INITIAL ESTRUCTURA
    '''
    p[0] = nodo("INITIAL") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    



def p_INITIAL_INICIAL(p):
    '''
    INITIAL : ESTRUCTURA
    '''
    p[0] = nodo("INITIAL") 
    p[0].agregar_hijo(p[1])

def p_ESTRUCTURA(p):
    '''
    ESTRUCTURA : PRODIF_ELSE
               | PRODIF
               | PRODDO_WHILE
               | PRODWHILE
               | PRODVOID
               | PRODFUNCION
               | DECLARACION
               | LLAMADA
                 
    '''
    p[0] = nodo("ESTRUCTURA") 
    p[0].agregar_hijo(p[1])
    

def p_ESTRUCTURA_PRODDO_WHILE(p):
    '''
    PRODDO_WHILE : reservada_do INSTRUCCIONES_FACTORIZADO reservada_while OPERACION_FACTORIZADO punto_coma
    '''
    p[0] = nodo("PRODDO_WHILE") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    p[0].agregar_hijo(p[4])
    p[0].agregar_hijo(p[5])

def p_ESTRUCTURA_PRODWHILE(p):
    '''
    PRODWHILE : reservada_while OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO 
    '''
    p[0] = nodo("PRODWHILE") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    
def p_ESTRUCTURA_IF_ELSE(p):
    '''
    PRODIF_ELSE : reservada_if OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO reservada_else INSTRUCCIONES_FACTORIZADO
    '''
   
    p[0] = nodo("PRODIF_ELSE") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    p[0].agregar_hijo(p[4])
    p[0].agregar_hijo(p[5])
    
def p_ESTRUCTURA_IF(p):
    '''
    PRODIF : reservada_if OPERACION_FACTORIZADO INSTRUCCIONES_FACTORIZADO
    '''
    p[0] = nodo("PRODIF") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
   
def p_ESTRUCTURA_VOID(p):
    '''
    PRODVOID : reservada_void id PARAMETROS_FACTORIZADO INSTRUCCIONES_FACTORIZADO
    '''
    p[0] = nodo("PRODVOID") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    p[0].agregar_hijo(p[4])

def p_ESTRUCTURA_FUNCION(p):
    '''
    PRODFUNCION : TIPO_DATO id PARAMETROS_FACTORIZADO INSTRUCCIONES_FACTORIZADO
    '''
    p[0] = nodo("PRODFUNCION") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    p[0].agregar_hijo(p[4])

def p_OPERACIONES(p):
    '''
    OPERACIONES : OPERACIONES OPERACION
    '''
    p[0] = nodo("OPERACIONES") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])  

def p_OPERACIONES_AUX(p):
    '''
     OPERACIONES : OPERACION 
    '''
    p[0] = nodo("OPERACIONES") 
    p[0].agregar_hijo(p[1])
    
def p_OPERACION_TRES(p):
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
    '''
    p[0] = nodo("OPERACION") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2]) 
    p[0].agregar_hijo(p[3])

def p_OPERACION_UNO(p):           
    '''
        OPERACION : numero
    '''

    p[0] = nodo("OPERACION") 
    p[0].agregar_hijo(p[1])

    
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
    p[0] = nodo("INSTRUCCIONES") 
    p[0].agregar_hijo(p[1])

def p_DECLARACIONES(p):
    '''
    DECLARACION : TIPO_DATO id operador_igual DATO punto_coma
    '''
    p[0] = nodo("DECLARACION") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    p[0].agregar_hijo(p[4])
    p[0].agregar_hijo(p[5])
    

def p_ASIGNACION(p):
    '''
    ASINGACION : id operador_igual DATO punto_coma
    '''
    p[0] = nodo("ASINGACION") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    p[0].agregar_hijo(p[4])

def p_TIPO_DATO(p):
    '''
    TIPO_DATO : tipo_int 
                | tipo_double
                | tipo_string
                | tipo_char
                | tipo_boolean
    
    '''
    p[0] = nodo("TIPO_DATO") 
    p[0].agregar_hijo(p[1])
def p_DATO(p):
    '''
    DATO : numero 
            | dato_double
            | dato_string
            | dato_char
            | dato_boolean_true
            | dato_boolean_false
    '''

    p[0] = nodo("DATO") 
    p[0].agregar_hijo(p[1])
def p_PARAMETRO_DEFINICION(p):
    '''
    PARAMETRO : TIPO_DATO id
    '''
    p[0] = nodo("PARAMETRO") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
def p_PARAMETROS_RECURSIVO(p):
    '''
    PARAMETROS :  PARAMETROS coma PARAMETRO 
    '''
    p[0] = nodo("PARAMETRO") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])

def p_PARAMETROS_RECURSIVO_AUX_1(p): 
    '''
    PARAMETROS :  PARAMETRO 
    '''
    p[0] = nodo("PARAMETROS") 
    p[0].agregar_hijo(p[1])

def p_PARAMETROS_RECURSIVO_AUX_2(p): 
    '''
    PARAMETROS :   
    '''
    p[0] = nodo("epsilon") 


def p_LLAMADA(p):
    '''
    LLAMADA : id parentesis_abre ARGUMENTOS parentesis_cierra
    '''
    p[0] = nodo("LLAMADA") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
    p[0].agregar_hijo(p[4]) 

def p_ARGUMENTOS(p):    #!##########################################################################
    '''
    ARGUMENTOS :  ARGUMENTOS coma ARGUMENTO 
    '''
    p[0] = nodo("ARGUMENTOS") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])

def p_ARGUMENTOS_AUX_1(p):
    '''
    ARGUMENTOS :  ARGUMENTO
    ''' 
    p[0] = nodo("ARGUMENTOS") 
    p[0].agregar_hijo(p[1])

def p_ARGUMENTOS_AUX_2(p): 
    '''
    ARGUMENTOS :  
    ''' 
    p[0] = nodo("epsilon") 

def p_ARGUMENTO(p):
    ''' 
    ARGUMENTO :  DATO
    '''
    p[0] = nodo("ARGUMENTO") 
    p[0].agregar_hijo(p[1])

def p_RETURN(p):
    '''
    RETURN : reservada_return punto_coma 
    '''
    p[0] = nodo("RETURN") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])

def p_RETURN_AUX(p):
    '''
    RETURN : reservada_return DATO punto_coma 
    '''
    p[0] = nodo("RETURN") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])



def p_BREAK(p):
    '''
    BREAK : reservada_break punto_coma 
    '''
    p[0] = nodo("BREAK") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
def p_CONTINUE(p):
    '''
    CONTINUE : reservada_continue punto_coma 
    '''
    p[0] = nodo("CONTINUE") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])









def p_FACTORIZACION_OPERACION(p):
    '''
    OPERACION_FACTORIZADO : parentesis_abre OPERACIONES parentesis_cierra
    '''
    p[0] = nodo("OPERACION_FACTORIZADO") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
def p_FACTORIZACION_INSTRUCCIONES(p):
    '''
    INSTRUCCIONES_FACTORIZADO : llave_abre INSTRUCCIONES llave_cierra
    '''
    p[0] = nodo("INSTRUCCIONES_FACTORIZADO") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])
def p_FACTORIZACION_PARAMETROS(p):
    '''
    PARAMETROS_FACTORIZADO : parentesis_abre PARAMETROS parentesis_cierra
    '''
    p[0] = nodo("PARAMETROS_FACTORIZADO") 
    p[0].agregar_hijo(p[1])
    p[0].agregar_hijo(p[2])
    p[0].agregar_hijo(p[3])



def p_error(p):
    if p:
        print(f"Sintaxis no válida cerca de '{p.value}' ({p.type})")
    else:
        print("Ninguna instrucción válida")


lexer = lex()
parser = yacc()
# lexer.lex(reflags=re.IGNORECASE)  # case insensitive


with open(input("introdusca el nombre del archivo :")+".sc") as f:
            print("archivo.sc aceptado ")
            msg = f.read()
INPUT = msg

ast = parser.parse(INPUT, lexer)

#print(json.dumps(ast, indent=10, sort_keys=False))




#! ARBOL SINTACTICO















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
f = open (input("introdusca el nombre del reporte HTML :")+".html",'w')
f.write(final)
f.close()


