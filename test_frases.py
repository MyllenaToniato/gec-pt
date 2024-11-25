import unittest
import sys, os
sys.path.append(os.pardir)

from Leitura04 import extrair_sentencas, ler_arquivo_xml

class TestCaseFrases(unittest.TestCase):

    def test_frases_corretas_erradas(self):

        sentencas = extrair_sentencas(ler_arquivo_xml("data/sample_test_frases.xml"))
        sentencas_alvo = ["De fato, estes não curam a<wrong>doença</wrong><correct>doença,</correct> apenas retardam seus danos e, mesmo com o seu uso, a AIDS é muito devastadora e a própria química forte dos remédios tem efeitos negativos sobre o organismo, mas em escala muito menor que a enfermidade.",
                          "A principal desculpa para não<wrong>usar-se</wrong><correct>se usar</correct>camisinha é a confiança no parceiro, porém, ele pode ter contraído o HIV anteriormente e não saber, pois, às vezes, o vírus permanece no corpo por anos antes <wrong>da</wrong><correct>de a</correct>doença se manifestar.",
                          "Com a efemeridade dos relacionamentos atuais, há casos<wrong>onde</wrong><correct>em que</correct>a pessoa tem relações com muitas outras, espalhando a doença antes de descobrir que a tem."]
        self.assertEqual(sentencas, sentencas_alvo)  # add assertion here





if __name__ == '__main__':
    unittest.main()
