from leitura07 import extrair_sentencas, ler_arquivo_xml

sentencas = extrair_sentencas(
            ler_arquivo_xml("../../IFES_correcao/aes-pt/data/data/a-aids-nao-e-mais-a-mesma-por-que-diminuiu-o-medo-da-doenca/xml/a-aids-ainda-nao-acabou.xml"))

print(sentencas)
