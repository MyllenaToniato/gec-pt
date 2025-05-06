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


### SENTENÇAS COM ERROS ###
def extrair_sentencas_com_erro(body_text):
    """ Essa função primeiro está reconhecento as tags <wrong> para depois fazer a tokenização"""
    trechos_com_tags = re.findall(
        r'([^.]*?<(wrong|correct)>.*?</\2>[^.]*\.)', body_text, re.DOTALL)

    if not trechos_com_tags:
        return []

    frases_com_tags = []
    for trecho,_ in trechos_com_tags:
        frases_com_tags.extend(sent_tokenize(trecho))

    return frases_com_tags

### FUNÇÃO PARA REMOVER COLCHETES EXTREMOS ###
def remover_colchetes_extremos(texto):
    if texto.startswith("[") and texto.endswith("]"):
        return texto[1:-1]  # Remove apenas os colchetes das extremidades
    return texto  # Retorna o texto original se não tiver colchetes no início e no fim


####### SENTENÇAS SEM ERROS #######
def extrair_sentencas_sem_erros(body_text):
    """Retorna as sentenças que não contêm as tags <wrong> ou <correct>"""
    frases = sent_tokenize(body_text)
    frases_sem_erros = [frase for frase in frases if not re.search(r'</?(wrong|correct)>', frase)]
    return frases_sem_erros

def varrer_arquivos_unificado(diretorio_base, arquivo_saida):
    """Varre os arquivos XML e salva frases com e sem erro em um único CSV com indicação"""
    dados = []

    for raiz, _, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.xml') and not arquivo.startswith('.') and arquivo != "prompt.xml":
                caminho_arquivo = os.path.join(raiz, arquivo)
                body_text = ler_arquivo_xml(caminho_arquivo)

                # Frases com erro (contendo <wrong> ou <correct>)
                frases_com_erro = extrair_sentencas_com_erro(body_text)
                for frase in frases_com_erro:
                    dados.append([remover_colchetes_extremos(frase), arquivo, raiz, True])

                # Frases sem erro
                todas_frases = sent_tokenize(body_text)
                frases_sem_erro = [
                    frase for frase in todas_frases
                    if not re.search(r'</?(wrong|correct)>', frase)
                ]
                for frase in frases_sem_erro:
                    dados.append([remover_colchetes_extremos(frase), arquivo, raiz, False])

    # Salvando no CSV
    with open(arquivo_saida, 'w', newline='', encoding='utf-8-sig') as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t")
        writer.writerow(["Texto", "Arquivo", "Diretorio", "com_erro"])
        writer.writerows(dados)

    print(f"Arquivo unificado '{arquivo_saida}' criado com sucesso!")


### EXTRAINDO APENAS O QUE ESTÁ DENTRO DA TAG <wrong> ###
def varrer_arquivos_erros_dentro_wrong_com_frase(diretorio_base, arquivo_saida):
    """Varre os arquivos XML e extrai o conteúdo das tags <wrong> junto com a frase original"""
    dados = []

    for raiz, _, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.xml') and not arquivo.startswith('.') and arquivo != "prompt.xml":
                caminho_arquivo = os.path.join(raiz, arquivo)
                body_text = ler_arquivo_xml(caminho_arquivo)

                # Divide o texto em frases
                frases = sent_tokenize(body_text)

                for frase in frases:
                    # Encontra pares <wrong>...</wrong> <correct>...</correct>
                    padrao = r'<wrong>(.*?)</wrong>\s*<correct>(.*?)</correct>'
                    correspondencias = re.findall(padrao, frase, re.DOTALL)

                    for errado, correto in correspondencias:
                        erro_limpo = errado.strip()
                        correcao_limpa = correto.strip()
                        dados.append([erro_limpo, correcao_limpa, frase.strip(), arquivo, raiz])

    # Salvando no TSV
       with open(arquivo_saida, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["palavra_errada", "palavra_correta", "frase_original", "arquivo", "diretorio"])
        writer.writerows(dados)

    print(f"Arquivo '{arquivo_saida}' com erros e frases originais criado com sucesso!")

####### UTILIZANDO A FUNÇÃO ###############


DIRETORIO_RAIZ = r"C:\Users\jpgtb\OneDrive\Documentos\PythonScripts\IFES_correcao\aes-pt\data"
CSV_SAIDA_BD = "resultado_extrair_sentenca_wrongcorrect.tsv"
ARQUIVO_SAIDA_DENTRO_WRONG = "erros_wrong_correct_com_frase_original.tsv"

#varrer_arquivos_unificado(DIRETORIO_RAIZ, CSV_SAIDA_BD)
varrer_arquivos_erros_dentro_wrong_com_frase(DIRETORIO_RAIZ, ARQUIVO_SAIDA_DENTRO_WRONG)


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
