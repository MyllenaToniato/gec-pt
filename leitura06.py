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
