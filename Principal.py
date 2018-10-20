import processamento, filtros, saidas

processo = processamento.Processamento()
exportar = saidas.Saidas()

intervaloano = filtros.Filtros("ano", "intervalofechado", (1980, 2000))

dados1 = processo.producao_em_funcao_de("ano", "total", intervaloano)
exportar.configurar_textos("Ano", "Produção[T]", "Produção Total por Ano")
exportar.carregar_pontos(dados1, "1980-2000", "ano", "producao")
exportar.plotar()
exportar.gerar_planilha("Produção 1980-2000", dados1)