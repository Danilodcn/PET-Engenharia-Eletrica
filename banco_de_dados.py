import mysql.connector
import pandas as pd
import numpy as np

class BD:

    def __init__(self):
        self.mydb = mysql.connector.connect(host="localhost", user="hackathon", passwd="hackathon", database="hackathon_ficticio")
        self.cursor = self.mydb.cursor()

    def inserir_producao_csv(self, diretorio):
        dados = pd.read_csv(diretorio, encoding="ISO-8859-1", sep=";")
        dados["id"] = dados["id"].astype(np.int)
        dados["ano"] = dados["ano"].astype(np.int)
        dados["producao"] = dados["producao"].astype(np.float)
        dados["pescador"] = dados["pescador"].astype(np.int)
        dados["pescado"] = dados["pescado"].astype(np.int)
        dados["dia"] = dados["dia"].astype(np.int)
        dados["mes"] = dados["mes"].astype(np.int)
        dados["comprimentoembarcacao"] = dados["comprimentoembarcacao"].astype(np.float)
        dados["potenciamotor"] = dados["potenciamotor"].astype(np.float)


        total = len(dados["id"])
        for i in range(0, total):
            id = dados["id"][i]
            pescador = dados["pescador"][i]
            estado = dados["estado"][i]
            cidade = dados["cidade"][i]
            porto = dados["porto"][i]
            dia = dados["dia"][i]
            mes = dados["mes"][i]
            ano = dados["ano"][i]
            pescado = dados["pescado"][i]
            producao = dados["producao"][i]
            embarcacao = dados["embarcacao"][i]
            comprimentoembarcacao = dados["comprimentoembarcacao"][i]
            potenciamotor = dados["potenciamotor"][i]
            tipo = dados["tipo"][i]
            ambiente = dados["ambiente"][i]
            artepesca = dados["artepesca"][i]

            sql = "insert into producao values" \
            "(%d, %d, '%s', '%s', '%s', %d, %d, %d, %d, %f, '%s', %f, %f, '%s', '%s', '%s')" % \
            (id, pescador, estado, cidade, porto, dia, mes, ano, pescado, producao, embarcacao, comprimentoembarcacao,
            potenciamotor, tipo, ambiente, artepesca)

            self.cursor.execute(sql)
            self.mydb.commit()

            print("Inserido %d/%d" %(i+1, total))

    def retornar_dados(self, tabela, campos, filtros, ordem):
        sql = "select "
        sql += self.trabalhar_campos(campos)
        sql += "from %s " %(tabela)
        sql += self.trabalhar_filtros(filtros) + " "
        sql += self.trabalhar_ordem(ordem)
        self.cursor.execute(sql)
        dados = self.cursor.fetchall()
        return dados

    def processar_lista(self, campos, separador):
        retorno = ""
        total = len(campos)
        for i in range(0, total):
            retorno += campos[i]
            if (i < total - 1):
                retorno += separador

        return retorno

    def trabalhar_campos(self, campos):
        retorno = ""
        if(campos == None):
            return retorno
        return self.processar_lista(campos, ", ") + " "

    def trabalhar_ordem(self, ordem):
        retorno = ""
        if(ordem == None):
            return retorno
        return "order by " + ordem[0] + " " + ordem[1] + " "

    def trabalhar_filtros(self, filtros):
        retorno = ""

        if(filtros == None):
            return retorno

        return "where " + filtros.str

    def retornar_colunas(self):
        sql = "show columns from producao"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        colunas = []

        for res in resultado:
            colunas.append(res[0])

        return colunas

    def chave_estrangeira(self, tabela, vetor):
        retorno = []
        if(tabela == "pescadores"):
            alvo = "nome"
        else:
            alvo = "nomepopular"

        for id in vetor:
            sql = "select %s from %s where id = %d" %(alvo, tabela, id)
            self.cursor.execute(sql)
            retorno.append(self.cursor.fetchone()[0])

        return retorno




        

