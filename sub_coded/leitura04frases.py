
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
    labeled_sentences = []

    if body is not None and body.text:
        # Obtenha o texto completo
        texto_completo = body.text

        # Procura pelas tags <wrong> e <correct>
        wrong = body.find(".//wrong")
        correct = body.find(".//correct")

        if wrong is not None and correct is not None:
            # Garantir que o texto de wrong e correct seja string
            wrong_text = wrong.text if wrong.text is not None else ""
            correct_text = correct.text if correct.text is not None else ""

            # Cria a frase com o erro (mantendo o <wrong>)
            frase_incorreta = texto_completo.replace(wrong.tag, wrong_text, 1)

            # Cria a frase corrigida (substituindo o <wrong> por <correct>)
            frase_corrigida = texto_completo.replace(
                wrong.tag, correct_text, 1)

            # Adicionar ambas as frases ao array
            labeled_sentences.append(frase_incorreta)
            labeled_sentences.append(frase_corrigida)

    return labeled_sentences


"""
def extrair_sentencas(body):
    labeled_sentences = []

    if body is not None:
        # Extrai o texto completo, preservando a estrutura do XML
        texto_completo = "".join(body.itertext()).strip()

        # Localiza todas as tags <wrong> e <correct>
        wrong_tags = body.findall(".//wrong")
        correct_tags = body.findall(".//correct")

        if wrong_tags and correct_tags:
            for wrong, correct in zip(wrong_tags, correct_tags):
                # Substitui apenas o conteúdo de <wrong> e <correct>
                wrong_text = f"<wrong>{
                    wrong.text.strip()}</wrong>" if wrong.text else "<wrong></wrong>"
                correct_text = f"<correct>{correct.text.strip(
                )}</correct>" if correct.text else "<correct></correct>"

                # Cria as versões das frases com erro e corrigidas
                frase_incorreta = texto_completo.replace(
                    wrong.text.strip(), wrong_text, 1)
                frase_corrigida = texto_completo.replace(
                    wrong.text.strip(), correct_text, 1)

                # Adiciona as frases ao array
                labeled_sentences.append(frase_incorreta.strip())
                labeled_sentences.append(frase_corrigida.strip())

    # Remove quebras de linha extras
    return [s.replace('\n', ' ').strip() for s in labeled_sentences]
"""

def percorrer_pastas(caminho_base):
    # Percorre as pastas e arquivos XML no caminho base e extrai sentenças
    labeled_senteces_total = []

    for root_dir, dirs, files in os.walk(caminho_base):
        for file in files:
            if file.endswith('.xml'):
                caminho_arquivo = os.path.join(root_dir, file)
                body = ler_arquivo_xml(caminho_arquivo)

                if body is not None:
                    labeled_senteces = extrair_sentencas(
                        body)
                    labeled_senteces_total.extend(labeled_senteces)

    return labeled_senteces_total


def main():
    nltk.download('punkt')

    # Solicita o caminho base
    caminho_base = input("Digite o caminho base para percorrer as pastas: ")

    if verificar_caminho(caminho_base):
        labeled_senteces = percorrer_pastas(caminho_base)

        print("Sentenças: ", labeled_senteces)


if __name__ == "__main__":
    main()
