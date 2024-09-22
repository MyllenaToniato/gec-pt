import os
import xml.etree.ElementTree as ET
from nltk.tokenize import sent_tokenize, word_tokenize

# Caminho inicial para percorrer as pastas
caminho_base = 'C:\\Users\\jpgtb\\OneDrive\\Documentos\\PythonScripts\\IFES_correcao\\aes-pt\\data\\data'

# listas contendo as sentenças
wrongSentences = []
correctSentences = []

# Me dá impressão que dá pra transformar algumas coisas em função, Akylanne. Tentei fazer, mas
# ficou ruim, não capturou todas as linhas, somente uma (acho que do jeito que fiz eu acabei
# resetando a variável ao invés de dar append)

# Rodando as pastas
for root_dir, dirs, files in os.walk(caminho_base):
    for file in files:
        # Busca o xml
        if file.endswith('.xml'):
            caminho_arquivo = os.path.join(root_dir, file)

            try:
                tree = ET.parse(caminho_arquivo)
                root_xml = tree.getroot()
                body = root_xml.find('.//body')

                # apanhei nessa parte, o código retornava null. O chat me deu a luz, precisa colocar
                # essa condição is not None para não tentar fazer o append em valor nulo.
                if body is not None:
                    wrong = body.find(".//wrong")
                    if wrong is not None:
                        wrongSentences.append(wrong.text)

                    correct = body.find(".//correct")
                    if correct is not None:
                        correctSentences.append(correct.text)

                # Achei que iría utilizar a função iter para ler o arquivo,
                # mas deu pra fazer pelo body ali em cima
                # Não tirei do código, mas pode ficar a vontade para fazê-lo.
                """ for element in root_xml.iter():
                    root_xml.find(".//wrong").push()
                    root_xml.find(".//correct").push()
                    print(f'Arquivo: {caminho_arquivo}, Elemento Raiz: {
                        root_xml.tag}') """

            except ET.ParseError as e:
                print(f'Erro ao ler o arquivo {caminho_arquivo}: {e}')
print(correctSentences)
print(wrongSentences)


# O código está lendo os arquivos e salvando as tags wrong e correct nessas listas, não sei
# se é bem isso que a professora precisa.
