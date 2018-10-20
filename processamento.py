import banco_de_dados, numpy as np

class Processamento:

    def __init__(self):
        self.bd = banco_de_dados.BD()

    def inserir_producao_csv(self, arquivo):
        self.bd.inserir_producao_csv("./bases/" + arquivo + ".csv")

    def retornar_dados(self, campos, filtros, ordem=None):
        dados = self.bd.retornar_dados("producao", campos, filtros, ordem)
        retorno = {}
        if (campos[0] == "*"):
            campos = self.bd.retornar_colunas()

        total_campos = len(campos)
        for i in range(0, total_campos):
            retorno[campos[i]] = []

        for i in range(0, len(dados)):
            for e in range(0, total_campos):
                retorno[campos[e]].append(dados[i][e])

        if("pescado" in campos):
            retorno["pescado"] = self.bd.chave_estrangeira("pescados", retorno["pescado"])

        if("pescador" in campos):
            retorno["pescador"] = self.bd.chave_estrangeira("pescadores", retorno["pescador"])

        return retorno

    def media_producao(self, filtros = None):
        dados = self.bd.retornar_dados("producao", ["producao"], filtros, None)
        total = 0
        total_dados = len(dados)

        if(total_dados == 0):
            return 0

        for dado in dados:
            total += dado[0]
        return total/total_dados

    def producao_em_funcao_de(self, variavel, grandeza, filtros = None):
        dados = self.bd.retornar_dados("producao", ["producao", variavel], filtros, (variavel, "asc"))
        variavel_independente = []
        producao = []
        quantidade_entradas = []
        for dado in dados:
            if(not(dado[1]) in variavel_independente):
                variavel_independente.append(dado[1])
                producao.append(dado[0])
                quantidade_entradas.append(1)
            else:
                producao[-1] += dado[0]
                quantidade_entradas[-1] += 1

        if(variavel == "pescado"):
            variavel_independente = self.bd.chave_estrangeira("pescados", variavel_independente)

        elif(variavel == "pescador"):
            variavel_independente = self.bd.chave_estrangeira("pescadores", variavel_independente)

        if(grandeza == "media"):
            for i in range(0, len(producao)):
                producao[i] /= quantidade_entradas[i]
        return {"producao": producao, variavel:variavel_independente}

    def taxa_de_crescimento(self, filtros = None):
        dados = self.producao_em_funcao_de("ano", "total", filtros)
        total_anos = len(dados["ano"])

        anos = []
        crescimentos = []
        for i in range(0, total_anos - 1):
            crescimentos.append((dados["producao"][i+1] - dados["producao"][i])*100/dados["producao"][i])
            anos.append(dados["ano"][i+1])

        return {"crescimento": crescimentos, "ano": anos}

    def ajustar_modelo(self, var_independente, grandeza = "total", filtros = None):
        dados = self.producao_em_funcao_de(var_independente, grandeza, filtros)
        producao = np.array(dados["producao"])
        ano = np.array(dados[var_independente])
        r_linear,a_linear,b_linear = self.correlacao_e_regressao(ano, producao)

        producao_ln = np.log(producao)
        r_exp, a_exp, b_exp = self.correlacao_e_regressao(ano, producao_ln)
        a_exp = np.exp(a_exp)

        if(abs(r_linear) >= abs(r_exp)):
            return ("lin", r_linear, a_linear, b_linear, ano, producao)
        else:
            return ("exp", r_exp, a_exp, b_exp, ano, producao)

    def correlacao_e_regressao(self, x, y):
        n = len(x)
        media_x = np.mean(x)
        media_y = np.mean(y)

        sxy = np.sum(x*y) - n*media_x*media_y
        sxx = np.sum(x**2) - n*media_x**2
        syy = np.sum(y**2) - n*media_y**2

        r = sxy/np.sqrt(sxx*syy)
        b = sxy/sxx
        a = media_y - b * media_x

        return r, a, b

    def kg_por_dia(self, filtros):
        dados = self.producao_em_funcao_de("dia", "total", filtros)
        producao_acumulada = []
        dias_acumulados = []
        for i in range(0, len(dados["dia"])):
            producao_acumulada.append(sum(dados["producao"][0:i+1]))
            dias_acumulados.append(i+1)

        return {"producao_acumulada":producao_acumulada, "dias_de_pesca":dias_acumulados}













