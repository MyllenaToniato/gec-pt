import unittest

from leitura03 import extrair_sentencas
class TestCaseFrases(unittest.TestCase):
    def test_frases_corretas_erradas(self):
        body = """
        De fato, estes não curam a<wrong>doença</wrong>
        <correct>doença,</correct>
        apenas retardam seus danos e,
         mesmo com o seu uso, a AIDS é muito devastadora e a própria química forte dos remédios tem efeitos negativos sobre o organismo, mas em escala muito menor que a enfermidade. Mesmo com esses problemas, a banalização da doença é frequente e gera irresponsabilidades, como não usar preservativos. A principal desculpa para não<wrong>usar-se</wrong>
        <correct>se usar</correct>
        camisinha é a confiança no parceiro, porém, ele pode ter contraído o HIV anteriormente e não saber, pois, às vezes, o vírus permanece no corpo por anos antes
        <wrong>da</wrong>
        <correct>de a</correct>
        doença se manifestar. Com a efemeridade dos relacionamentos atuais, há casos
        <wrong>onde</wrong>
        <correct>em que</correct>
        a pessoa tem relações com muitas outras, espalhando a doença antes de descobrir que a tem. Portanto, o fato de conhecer o outro e a aparência saudável deste não fazem uma relação sexual ser necessariamente segura.
         Enquanto a ciência, que tem trabalhado arduamente, não encontra a cura e a vacina da Aids é fundamental alertar a população, por meio de campanhas na mídia e nas escolas, a fim de impedir que o descaso e a falta de informação espalhem mais ainda esse mal.
        """
        sentencas = extrair_sentencas(body)
        sentencas_alvo = ["De fato, estes não curam a<wrong>doença</wrong><correct>doença,</correct> apenas retardam seus danos e, mesmo com o seu uso, a AIDS é muito devastadora e a própria química forte dos remédios tem efeitos negativos sobre o organismo, mas em escala muito menor que a enfermidade.",
                          "A principal desculpa para não<wrong>usar-se</wrong><correct>se usar</correct>camisinha é a confiança no parceiro, porém, ele pode ter contraído o HIV anteriormente e não saber, pois, às vezes, o vírus permanece no corpo por anos antes <wrong>da</wrong><correct>de a</correct>doença se manifestar.",
                          "Com a efemeridade dos relacionamentos atuais, há casos<wrong>onde</wrong><correct>em que</correct>a pessoa tem relações com muitas outras, espalhando a doença antes de descobrir que a tem."]
        self.assertEqual(sentencas, sentencas_alvo)  # add assertion here


if __name__ == '__main__':
    unittest.main()
