# CÓDIGO PARA GERAR AS ESTATÍSTICAS#
import csv
from collections import Counter
import re
import statistics
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

## FUNÇÃO PARA EXTRAIR AS FRASES ERRADAS ##
def extrair_palavras_erradas(frases):
    erros = []

    for frase in frases:
        # Encontra todos os trechos dentro de <wrong>...</wrong>
        encontrados = re.findall(r'<wrong>(.*?)</wrong>', frase)
        for trecho in encontrados:
            palavras = word_tokenize(trecho)
            palavras_filtradas = [
                p for p in palavras
                if re.match(r'^[\wÀ-ÿ]+$', p) and p.lower() not in stopwords.words('portuguese')]
            erros.extend(palavras_filtradas)

    return erros


### FUNÇÃO PARA COMPUTAR AS ESTATÍSTICAS E GERAR UM CSV ### 
def executar_estatisticas_gerais(caminho_arquivo_tsv):
    df = pd.read_csv(caminho_arquivo_tsv, sep='\t')

    # Estatísticas gerais por tipo de frase
    estatisticas_frases(df, com_erro=True)
    estatisticas_frases(df, com_erro=False)

    # Extração de palavras com erro
    df_com_erro = df[df['com_erro']]
    palavras_erradas = extrair_palavras_erradas(df_com_erro['Texto'])
    contagem_erros = Counter(palavras_erradas).most_common(20)

    print("\n=== PALAVRAS COM ERRO MAIS FREQUENTES ===")
    for palavra, freq in contagem_erros:
        print(f"{palavra}: {freq}")

    # Salvando CSV das palavras com erro
    with open("palavras_erradas_mais_frequentes.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Palavra_Errada", "Frequencia"])
        writer.writerows(contagem_erros)

    print("Arquivo 'palavras_erradas_mais_frequentes.csv' salvo com sucesso!")




# FUNÇÃO PARA IGNORAR ADVERBOS, PREPOSIÇÕES E STOPWORDS
def filtrar_palavras(palavras):
    """Remove pontuação, advérbios, preposições, artigos e stopwords"""
    palavras = [p for p in palavras if re.match(r'^[\wÀ-ÿ]+$', p)]  # remove pontuações
    stopwords_pt = set(stopwords.words('portuguese')) # É melhor usar pos_tag(palavras, lang='por'), porém não há suporte para PT.
    # Remove palavras que são stopwords (como preposições e advérbios mais comuns)
    palavras_filtradas = [palavra for palavra in palavras if palavra.lower() not in stopwords_pt]

    return palavras_filtradas

### FUNÇÃO PARA CALCULAR ESTATÍSTICAS, MAS NÃO FICOU LEGAL##
def estatisticas_frases(df, com_erro=True):
   #Calcula estatísticas para frases com ou sem erro
    if com_erro:
        frases = df[df['Texto'].str.contains(
            r'</?(wrong|correct)>', regex=True)]['Texto']
    else:
        frases = df[~df['Texto'].str.contains(
            r'</?(wrong|correct)>', regex=True)]['Texto']

    total_frases = len(frases)
    comprimento_frases = []
    palavras_total = []

    for frase in frases:
        frase_limpa = re.sub(r'</?[^>]+>', '', frase)  # remove tags <wrong>, <correct>
        palavras = word_tokenize(frase_limpa)
        palavras_filtradas = filtrar_palavras(palavras) 
        palavras_total.extend(palavras_filtradas)
        comprimento_frases.append(len(palavras_filtradas))

    media = statistics.mean(comprimento_frases) if comprimento_frases else 0
    mediana = statistics.median(
        comprimento_frases) if comprimento_frases else 0
    try:
        moda = statistics.mode(comprimento_frases)
    except statistics.StatisticsError:
        moda = 'Nenhuma moda'
    desvio = statistics.stdev(comprimento_frases) if len(
        comprimento_frases) > 1 else 0
    frequencia_palavras = Counter(palavras_total).most_common(10)

    tipo = "COM ERRO" if com_erro else "SEM ERRO"
    print(f"\n=== ESTATÍSTICAS PARA FRASES {tipo} ===")
    print(f"Total de frases: {total_frases}")
    print(f"Média de palavras por frase: {media:.2f}")
    print(f"Mediana: {mediana}")
    print(f"Moda: {moda}")
    print(f"Desvio padrão: {desvio:.2f}")
    print(f"Palavras mais frequentes: {frequencia_palavras}")


## Gerar estatísticas CSV
def gerar_estatisticas_csv(df, arquivo_saida_csv):
    estatisticas = []

    for com_erro_flag in [True, False]:
        subset = df[df['com_erro'] == com_erro_flag]
        tipo = "COM_ERRO" if com_erro_flag else "SEM_ERRO"

        comprimento_frases = []
        for frase in subset['Texto']:
            frase_limpa = re.sub(r'</?[^>]+>', '', frase)
            palavras = word_tokenize(frase_limpa)
            comprimento_frases.append(len(palavras))

        if comprimento_frases:
            media = statistics.mean(comprimento_frases)
            mediana = statistics.median(comprimento_frases)
            try:
                moda = statistics.mode(comprimento_frases)
            except statistics.StatisticsError:
                moda = 'Nenhuma moda'
            desvio = statistics.stdev(comprimento_frases) if len(comprimento_frases) > 1 else 0
        else:
            media = mediana = desvio = 0
            moda = 'Sem dados'

        estatisticas.append({
            "tipo": tipo,
            "total_frases": len(comprimento_frases),
            "media_palavras_por_frase": round(media, 2),
            "mediana_palavras_por_frase": mediana,
            "moda_palavras_por_frase": moda,
            "desvio_padrao_palavras_por_frase": round(desvio, 2)
        })

    estat_df = pd.DataFrame(estatisticas)
    estat_df.to_csv(arquivo_saida_csv, index=False, encoding='utf-8-sig')
    print(f"Arquivo de estatísticas salvo em '{arquivo_saida_csv}' com sucesso!")


## EXECUTANDO A ESTATÍSTICA ##

executar_estatisticas_gerais("resultado_extrair_sentenca_erro_semerro.tsv")


"""
df = pd.read_csv('resultado_extrair_sentenca_erro_semerro.tsv', sep='\t')
df_com_erro = df[df['com_erro']]
palavras_erradas=extrair_palavras_erradas(df_com_erro['Texto'])
contagem_erros = Counter(palavras_erradas).most_common(20)
print("Palavras com erro mais frequentes:")
for palavra, freq in contagem_erros:
    print(f"{palavra}: {freq}")

estatisticas_frases(df, com_erro=True)  # frase com erro
estatisticas_frases(df, com_erro=False)  # frase sem erro
"""
