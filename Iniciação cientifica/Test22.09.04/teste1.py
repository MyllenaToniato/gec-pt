import os
import xml.etree.ElementTree as ET

# Função para ler e extrair texto de um arquivo XML
def extrair_texto_xml(Users\\PICHAU\\Documents\\Prog001\\data\\a-aids-nao-e-mais-a-mesma-por-que-diminuiu-o-medo-da-doenca\\xml):
    tree = ET.parse(Users\PICHAU\Documents\Prog001\data\a-aids-nao-e-mais-a-mesma-por-que-diminuiu-o-medo-da-doenca\xml)  # Carrega o XML
    root = tree.getroot()  # Obtém o elemento raiz
    texto = ""
    
    # Percorre todos os elementos do XML e concatena o texto encontrado
    for elem in root.iter():
        if elem.text:
            texto += elem.text.strip() + " "
    
    return texto