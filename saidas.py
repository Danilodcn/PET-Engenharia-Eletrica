import pylab as plot
import xlwt
import numpy as np

class Saidas:

    def __init__(self):
        self.legendas = []
        self.barras = []
        plot.grid(True)

    def configurar_textos(self, eixo_x, eixo_y, titulo):
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.titulo = titulo

    def carregar_pontos(self, dados, nome, eixo_x, eixo_y):
        plot.plot(dados[eixo_x], dados[eixo_y], "o")
        self.legendas.append(nome)

    def carregar_curva(self, dados, nome, eixo_x, eixo_y):
        plot.plot(dados[eixo_x], dados[eixo_y], marker="o")
        self.legendas.append(nome)

    def plotar(self):
        plot.legend(self.legendas)
        plot.title(self.titulo)
        plot.xlabel(self.eixo_x)
        plot.ylabel(self.eixo_y)
        plot.grid(True)
        plot.show()

    def gerar_planilha(self, nome, dados):
        book = xlwt.Workbook()
        folha1 = book.add_sheet(nome)
        linha = folha1.row(0)
        colunas = list(dados.keys())
        qtd_colunas = len(colunas)
        for i in range(0, qtd_colunas):
            linha.write(i, colunas[i])

        for i in range(0, len(dados[colunas[0]])):
            linha = folha1.row(i+1)
            for e in range(0, qtd_colunas):
                linha.write(e, dados[colunas[e]][i])

        book.save("./Tabelas/" + nome + ".xls")

    def ajuste_pontos(self, modelo):
        tipo = modelo[0]
        a = modelo[2]
        b = modelo[3]
        eixo_x = modelo[4]
        eixo_y = modelo[5]

        plot.scatter(eixo_x, eixo_y)



        if(tipo == "lin"):
            funcao = lambda x: a + x*b
        else:
            funcao = lambda x: a*np.exp(b*x)

        funcao_vetorizada = np.vectorize(funcao)

        x = np.arange(eixo_x[0], eixo_x[-1] + 1, 1)
        y = funcao_vetorizada(x)

        plot.plot(x,y, "r--")
        self.legendas += ["Curva Ajustada", "Diagrama de Dispersão"]

    def planilha_ajuste(self, modelo):
        tipo = modelo[0]
        r = modelo[1]
        a = modelo[2]
        b = modelo[3]

        if(tipo == "exp"):
            tipo = "y = a*e^(b*x)"
        else:
            tipo = "y = a + b*x"

        dados_para_planilha = {"tipo":[tipo], "r": [r], "a": [a], "b": [b]}
        self.gerar_planilha("Ajuste de Curva", dados_para_planilha)
