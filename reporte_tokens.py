class clase_token:
    def __init__(self,linea,columna,token,tipo,iteraciones):
        self.linea=linea
        self.columna=columna
        self.token=token
        self.tipo=tipo
        
        
       
        


    def html(self):
        return "<tr class=\"active-row\">" + "<td>"+ str(self.linea)+"</td>" + "<td>"+ str(self.columna)+"</td>" + "<td>"+ str(self.token)+"</td>"+"<td>"+ str(self.tipo)+"</td>" +"</tr>"