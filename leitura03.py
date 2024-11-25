import nltk
from nltk.tokenize import sent_tokenize
import os
import xml.etree.ElementTree as ET

nltk.download('punkt_tab')

def verificar_caminho(caminho_base):
    # Verifica se o caminho fornecido existe
    if not os.path.exists(caminho_base):
        print(f'O caminho {caminho_base} não existe.')
        return False
    return True


def ler_arquivo_xml(caminho_arquivo):
    # Lê um arquivo XML e retorna o corpo do XML se existir
    try:
        tree = ET.parse(caminho_arquivo)
        root_xml = tree.getroot()
        body = root_xml.find('.//body')
        return body
    except ET.ParseError as e:
        print(f'Erro ao ler o arquivo {caminho_arquivo}: {e}')
        return None


def extrair_sentencas(body):
    # Extrai as sentenças e verifica se contêm <wrong> e <correct>
    labeled_sentences = []

    if body is not None and body.text:

        sentencas = sent_tokenize(body.text)

        for sentenca in sentencas:
            if "<wrong>" and "<correct>" in sentenca:
                labeled_sentences.append(sentenca)

    return labeled_sentences


def percorrer_pastas(caminho_base):
    # Percorre as pastas e arquivos XML no caminho base e extrai sentenças
    labeled_sentences_total = []

    for root_dir, files in os.walk(caminho_base):
        for file in files:
            if file.endswith('.xml'):
                caminho_arquivo = os.path.join(root_dir, file)
                body = ler_arquivo_xml(caminho_arquivo)

                if body is not None:
                    labeled_sentences = extrair_sentencas(
                        body)
                    labeled_sentences_total.extend(labeled_sentences)

    return labeled_sentences_total


def main():
    nltk.download('punkt')

    # Solicita o caminho base
    caminho_base = input("Digite o caminho base para percorrer as pastas: ")

    if verificar_caminho(caminho_base):
        wrong_sentences, correct_sentences = percorrer_pastas(caminho_base)

        print("Sentenças incorretas: ", wrong_sentences)
        print("Sentenças corretas: ", correct_sentences)


if __name__ == "__main__":
    main()
