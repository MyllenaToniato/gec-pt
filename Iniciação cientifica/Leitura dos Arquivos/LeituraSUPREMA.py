import nltk
from nltk.tokenize import sent_tokenize
import os
import xml.etree.ElementTree as ET

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

    for root_dir, _, files in os.walk(caminho_base):
        for file in files:
            if file.endswith('.xml'):
                caminho_arquivo = os.path.join(root_dir, file)
                body = ler_arquivo_xml(caminho_arquivo)

                if body is not None:
                    labeled_sentences = extrair_sentencas(body)
                    labeled_sentences_total.extend(labeled_sentences)

    return labeled_sentences_total

def formato_Bio(sentenca):
    palavras = sentenca.split()
    bio_formato = []

    tag_interior = bool(False)
    tipo_tag = ""

    for palavra in palavras:
        if "<wrong>" in palavra:
            tipo_tag = "WRONG"
            palavra = palavra.replace("<wrong>", "")
            bio_formato.append(f"{palavra} B-{tipo_tag}")
            tag_interior = True
        elif "</wrong>" in palavra:
            palavra = palavra.replace("</wrong>", "")
            bio_formato.append(f"{palavra} I-{tipo_tag}")
            tag_interior = False
        elif "<correct>" in palavra:
            tipo_tag = "CORRECT"
            palavra = palavra.replace("<correct>", "")
            bio_formato.append(f"{palavra} B-{tipo_tag}")
            tag_interior = True
        elif "</correct>" in palavra:
            palavra = palavra.replace("</correct>", "")
            bio_formato.append(f"{palavra} I-{tipo_tag}")
            tag_interior = False
        else:
            if tag_interior:
                bio_formato.append(f"{palavra} I-{tipo_tag}")
            else:
                bio_formato.append(f"{palavra} O")

    return bio_formato

def bio_to_txt(sentencas, arquivo_saida):
    with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
        for sentenca in sentencas:
            resultado_bio = formato_Bio(sentenca)
            for linha in resultado_bio:
                arquivo.write(linha + "\n")

def main():
    nltk.download('punkt')

    # Solicita o caminho base e arquivo de saída
    caminho_base = input("Digite o caminho base para percorrer as pastas: ")
    arquivo_saida = input("Digite o nome do arquivo de saída (ex: resultado.txt): ")

    if verificar_caminho(caminho_base):
        labeled_sentences = percorrer_pastas(caminho_base)
        bio_to_txt(labeled_sentences, arquivo_saida)
        print(f"Processo concluído. Sentenças BIO salvas em {arquivo_saida}.")

if __name__ == "__main__":
    main()
