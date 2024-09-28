from nltk.tokenize import sent_tokenize, word_tokenize
import os
import xml.etree.ElementTree as ET

#-------------------------------------------------

def verificar_caminho(caminho_base):
    #Verifica se o caminho fornecido pelo usuário existe.
    if not os.path.exists(caminho_base):
        print(f'O caminho {caminho_base} não existe.')
        return False
    return True



def ler_arquivo_xml(caminho_arquivo):
    #Lê um arquivo XML e retorna o corpo do XML se existir.
    try:
        tree = ET.parse(caminho_arquivo)
        root_xml = tree.getroot()
        body = root_xml.find('.//body')
        return body
    except ET.ParseError as e:
        print(f'Erro ao ler o arquivo {caminho_arquivo}: {e}')
        return None
    


def extrair_sentencas(body):
    #Extrai as sentenças 'wrong' e 'correct' de um corpo XML.
    wrong_sentences = []
    correct_sentences = []

    if body is not None:
        wrong = body.find(".//wrong")
        if wrong is not None:
            wrong_sentences.append(wrong.text)

        correct = body.find(".//correct")
        if correct is not None:
            correct_sentences.append(correct.text)

    return wrong_sentences, correct_sentences




def imprimir_body(body, caminho_arquivo):
    #Imprime o conteúdo do body do arquivo XML
    if body is not None:
        body_content = ET.tostring(body, encoding='utf-8').decode('utf-8')
        print(f"Conteúdo do <body> do arquivo '{caminho_arquivo}':")
        print(body_content)
    else:
        print(f"O arquivo '{caminho_arquivo}' não contém um <body>.")



def percorrer_pastas(caminho_base):
    #Percorre as pastas e arquivos XML no caminho base e extrai sentenças
    wrong_sentences_total = []
    correct_sentences_total = []

    for root_dir, dirs, files in os.walk(caminho_base):
        for file in files:
            if file.endswith('.xml'):
                caminho_arquivo = os.path.join(root_dir, file)
                body = ler_arquivo_xml(caminho_arquivo)

                if body is not None:
                    # Imprime o conteúdo do body diretamente ao ler o arquivo
                    imprimir_body(body, caminho_arquivo)

                    # Extrai e acumula as sentenças 'wrong' e 'correct'
                    wrong_sentences, correct_sentences = extrair_sentencas(body)
                    wrong_sentences_total.extend(wrong_sentences)
                    correct_sentences_total.extend(correct_sentences)

    return wrong_sentences_total, correct_sentences_total



def main():
    
    # Solicita o caminho base ao 
    caminho_base = input("Digite o caminho base para percorrer as pastas: ")

    # Verifica se o caminho é válido
    if verificar_caminho(caminho_base):
        wrong_sentences, correct_sentences = percorrer_pastas(caminho_base)

        # Imprime sentenças incorretas e corretas
        print("Sentenças incorretas:", wrong_sentences)
        print("Sentenças corretas:", correct_sentences)

if __name__ == "__main__":
    main()
