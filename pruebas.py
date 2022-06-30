from graphviz import Source


inicio = """digraph html {"""
final ="""}"""
 
medio = """ A [label="King Arthur"]
    B [label="Sir Bedevere the Wise"]
    L [label="Sir Lancelot the Brave"]
    A -> B
    A -> L
    B -> L [constraint=false]"""

documento = inicio + medio + final
g = Source(documento, filename="gola",format="pdf")
g.view()


"""puntero= self.end
dato_pizza=""
while puntero != None:
    print(puntero.dato)
    #!CONCATENACION             LETRA                       [label="King Arthur"]             
    dato_pizza= dato_pizza + "Q"+str(id(puntero.dato))+"[label=\""+puntero.dato.string()+"\"]\n"
    if puntero.anterior != None:
        dato_pizza=dato_pizza+"Q"+str(id(puntero.dato)) +"->"+"Q"+str(id(puntero.anterior.dato))+"\n"

    puntero = puntero.anterior

return dato_pizza"""
[['if', [[['5'], '*'], '+']], ['if', [['5'], '*']]]