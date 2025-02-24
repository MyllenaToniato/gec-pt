import os
import csv
from lxml import etree
from nltk.tokenize import sent_tokenize
import re


def ler_arquivo_xml(caminho_arquivo):
    """Abre o arquivo xml com base no caminho passado"""
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo_xml = arquivo.read()
    tree = etree.fromstring(conteudo_xml)
    body_element = tree.find('body')
    if body_element is None:
        return ""
    body_text = (body_element.text or '') + ''.join(etree.tostring(child,
                                                                   encoding='unicode') for child in body_element)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    return body_text


# ESSA FUNÇÃO NÃO ESTÁ ENCONTRANDO ALGUMAS TAGS <WRONG>. Ao que me parece, é um erro na tokenização,
# ela não extrai a sentença se a tag <wrong> se iniciar em um parágrafo e terminar em outro.
# def extrair_sentencas(body_text):
#    frases = sent_tokenize(body_text)
#    frases_com_erros = [frase for frase in frases if re.search(
#        r'<wrong>.*?</wrong>', frase, re.DOTALL)]
#    return frases_com_erros


def extrair_sentencas_novo(body_text):
    """ Essa função primeiro está reconhecento as tags <wrong> para depois fazer a tokenização"""
    trechos_com_tags = re.findall(
        r'([^.]*?<(wrong|correct)>.*?</\2>[^.]*\.)', body_text, re.DOTALL)

    if not trechos_com_tags:
        return []

    frases_com_tags = []
    for trecho,_ in trechos_com_tags:
        frases_com_tags.extend(sent_tokenize(trecho))

    return frases_com_tags


def remover_colchetes_extremos(texto):
    """Pode ser utilizado para remover os colchetes, se necessário"""
    if texto.startswith("[") and texto.endswith("]"):
        return texto[1:-1]  # Remove apenas os colchetes das extremidades
    return texto  # Retorna o texto original se não tiver colchetes no início e no fim


def varrer_arquivos(diretorio_base, arquivo_saida):
    """Varre as pastas iniciando na raiz e gera um CSV com os retornos"""
    dados = []

    for raiz, _, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.xml') and not arquivo.startswith('.') and arquivo != "prompt.xml":
                caminho_arquivo = os.path.join(raiz, arquivo)
                body_text = ler_arquivo_xml(caminho_arquivo)
                frases_com_erros = extrair_sentencas_novo(body_text)
                dados.append([frases_com_erros, arquivo, raiz])

                # if frases_com_erros:  # Verifica se a lista não está vazia
                #    dados.append([remover_colchetes_extremos(
                #        frases_com_erros[0]), arquivo, raiz])
                # else:
                # Adiciona uma lista vazia caso não haja frases com erro.# dados.append([frases_com_erros,arquivo,raiz])
                # dados.append([[], arquivo, raiz])
                # dados.append([remover_colchetes_extremos(frases_com_erros[0]), arquivo, raiz])
                # for frase in frases_com_erros:
                #    dados.append([frase, arquivo, raiz])


def varrer_arquivos_sem_colchetes(diretorio_base, arquivo_saida):
    """Varre as pastas iniciando na raiz e gera um CSV com os retornos. Adicionalmente, retira os colchetes """
    dados = []

    for raiz, _, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.xml') and not arquivo.startswith('.') and arquivo != "prompt.xml":
                caminho_arquivo = os.path.join(raiz, arquivo)
                body_text = ler_arquivo_xml(caminho_arquivo)
                frases_com_erros = extrair_sentencas_novo(body_text)

                if frases_com_erros:  # Verifica se a lista não está vazia
                    dados.append([remover_colchetes_extremos(
                        frases_com_erros[0]), arquivo, raiz])
                else:
                    # Adiciona uma lista vazia caso não haja frases com erro.
                    dados.append([[], arquivo, raiz])

    with open(arquivo_saida, 'w', newline='', encoding='utf-8-sig') as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t")
        writer.writerow(["Texto", "Arquivo", "Diretório"])
        writer.writerows(dados)

    print(f"Arquivo TSV '{arquivo_saida}' criado com sucesso!")

####### UTILIZANDO A FUNÇÃO ###############


DIRETORIO_RAIZ = r"C:\Users\jpgtb\OneDrive\Documentos\PythonScripts\IFES_correcao\aes-pt\data"
CSV_SAIDA = "resultado_extrair_sentenca_wrongcorrect.tsv"
CSV_SAIDA_SEM_COLCHETE = "resultado_extrair_sentenca_wrongcorrect_sem_colchetes.tsv"
# varrer_arquivos(DIRETORIO_RAIZ, CSV_SAIDA)
varrer_arquivos_sem_colchetes(DIRETORIO_RAIZ, CSV_SAIDA_SEM_COLCHETE)

###########################################

#### TESTES ####
# teste = ler_arquivo_xml(
#    "../../IFES_correcao/aes-pt/data/data/a-necessidade-de-crer-em-herois/xml/ult4657u28.xml")
# teste1 = ler_arquivo_xml(
#    "../../IFES_correcao/aes-pt/data/data/a-aids-nao-e-mais-a-mesma-por-que-diminuiu-o-medo-da-doenca/xml/a-aids-ainda-nao-acabou.xml")#
#
# padrao = r"<wrong>.*?</wrong>"
#
# texto = extrair_sentencas_novo(teste)
# texto1 = extrair_sentencas_novo(teste1)
# print(texto)
# print(texto1)

# frases_teste = sent_tokenize(teste)
# frases_erro_teste = []
# for frase in frases_teste:
#    print("teste:", re.search(padrao, frase, re.DOTALL))

# if re.search('<wrong>.*?</wrong>', frase):
#    frases_erro_teste.append(frase)
# print(frases_erro_teste)
