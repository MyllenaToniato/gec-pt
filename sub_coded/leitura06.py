from lxml import etree
from nltk.tokenize import sent_tokenize
import re
import xml.etree.ElementTree as ET


def ler_arquivo_xml(caminho_arquivo):
    # lê o arquivo xml
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo_xml = arquivo.read()
    tree = etree.fromstring(conteudo_xml)
    body_element = tree.find('body')
    body_text = (body_element.text or '') + ''.join(etree.tostring(child,
                                                                   encoding='unicode') for child in body_element)
    body_text = re.sub(r'\s+', ' ', body_text).strip()

    return body_text


def extrair_sentencas(body_text):
    # tokeniza o body encontrado na outra função com base na tag wrong
    frases = sent_tokenize(body_text)
    frases_com_erros = [frase for frase in frases if re.search(
        r'<wrong>.*?</wrong>', frase)]

    return frases_com_erros


def extrair_sentencas_novo(body_text):
    # Primeiro, extrai todas as ocorrências de <wrong> até </wrong> diretamente do texto
    trechos_com_wrong = re.findall(
        r'([^.]*?<wrong>.*?</wrong>[^.]*\.)', body_text, re.DOTALL)

    # Se não encontrar nada, retorna lista vazia
    if not trechos_com_wrong:
        return []

    # Tokeniza apenas as frases extraídas para garantir que mantêm a estrutura
    frases_com_erros = []
    for trecho in trechos_com_wrong:
        frases_com_erros.extend(sent_tokenize(trecho))

    return frases_com_erros

#### TESTE OUTPUT UMA REDAÇÃO ###
#sentencas = extrair_sentencas(
#            ler_arquivo_xml("../../IFES_correcao/aes-pt/data/data/a-aids-nao-e-mais-a-mesma-por-que-diminuiu-o-medo-da-doenca/xml/a-aids-ainda-nao-acabou.xml"))
#print(sentencas)