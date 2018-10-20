class Filtros:

    def __init__(self, campo = None, tipo = None, valor = None):
        self.str = ""
        if(type(valor) == int or type(valor) == float):
            valor = str(valor)
        if(tipo == "igual"):
            self.str += campo + "=" + valor

        if(tipo == "menor"):
            self.str += campo + "<" + valor

        if(tipo == "maior"):
            self.str += campo + ">" + valor

        if(tipo == "maiorigual"):
            self.str += campo + ">=" + valor

        if(tipo == "menorigual"):
            self.str += campo + "<=" + valor

        if(tipo == "diferente"):
            self.str += campo + "<>" + valor

        if(tipo == "intervalofechado"):
            self.str += campo + ">=" + str(valor[0]) + " and " + campo + "<=" + str(valor[1])

        if(tipo == "intervaloaberto"):
            self.str += campo + ">" + str(valor[0]) + " and " + campo + "<" + str(valor[1])

        if(tipo == "intervaloiniciofechado"):
            self.str += campo + ">=" + str(valor[0]) + " and " + campo + "<" + str(valor[1])

        if(tipo == "intervalofimfechado"):
            self.str += campo + ">" + str(valor[0]) + " and " + campo + "<=" + str(valor[1])

    def __mul__(self, outro):
        return Filtros.filtro_customizado(self.str + " and " + outro.str)

    def __add__(self, outro):
        return Filtros.filtro_customizado(self.str + " or " + outro.str)

    def __repr__(self):
        return self.str


    def filtracao_customizada(self, filtro):
        self.str = filtro

    @classmethod
    def filtro_customizado(cls, filtro):
        retorno = cls()
        retorno.filtracao_customizada(filtro)
        return retorno
