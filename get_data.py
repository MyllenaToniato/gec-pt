import pandas as pd
import re
from collections import Counter
from sklearn.model_selection import train_test_split

SEED = 100

# ********** FUNÇÃO PARA TRANSFORMAR AS SENTENÇAS COM TAGS EM SENTENÇAS EM FORMATO BIO **********

def tag2bio(sentenca):
    if not isinstance(sentenca, str):
        return []

    sent_temp = sentenca
    # ** Separação e armazenamento dos tokens **

    # Parte 1: Separação de todas as tags
    sent_temp2 = sent_temp
    for tag in ["<wrong>", "</wrong>", "<correct>", "</correct>"]:
        sent_temp2 = sent_temp2.replace(tag, " " + tag + " ")

    # Parte 2: Separação da pontuação
    sep_pont = ['.', ',', ';', ':', '?', '!', '(', ')', '[', ']', '{', '}', "'", '"']
    for pontuacao in sep_pont:
        sent_temp2 = sent_temp2.replace(pontuacao, " " + pontuacao + " ")

    # Parte 3: Guardar tokens separados
    sent_temp2 = re.sub(r'\s+', ' ', sent_temp2)

    tokens = []
    for token in sent_temp2.strip().split(' '):
        if token != "":
            tokens.append(token)

    # ** Transformar para tag BIO **
    bio = []
    trecho_errado = False
    primeiro_erro = True

    for token in tokens:
        if token == "<wrong>":
            trecho_errado = True
            primeiro_erro = True
        elif token == "</wrong>":
            trecho_errado = False
        else:
            if trecho_errado:
                if primeiro_erro:
                    bio.append((token, "B-WRONG"))
                    primeiro_erro = False
                else:
                    bio.append((token, "I-WRONG"))
            else:
                bio.append((token, "O"))

    return bio

# ********** FUNÇÃO PARA VERIFICAR SE A FRASE CONTÉM ERRO **********

def contem_erro(sentenca_bio):
    for _, tag in sentenca_bio:
        if 'WRONG' in tag:
            return True
    return False

# ********** FUNÇÃO PARA LER OS ARQUIVOS TEST.TSV E TRAIN.TSV E TRANSFORMAR AS SENTENÇAS EM FORMATO BIO **********

def analisa_estratificacao(arquivo):
    try:
        df = pd.read_csv(arquivo, encoding='latin-1', sep='\t')
    except FileNotFoundError:
        print ("Não foi possível ler os arquivos de treino e teste. Tente novamente.")
        return 1

    try:
        df['formato_bio_list'] = df['formato_bio'].apply(eval)
    except Exception as e:
        print(f"Erro ao converter 'formato_bio' em {arquivo}. Verifique o formato dos dados: {e}")
        return None, 0

# ********** FUNÇÃO PARA CALCULAR AS ESTATÍSTICAS DE CADA TOTAL E DE CADA TAG EM FORMATO BIO **********

def calcular_estatistica_bio (df):
    # 1. Extração das tags de cada token, usando cada conjunto de tokens e tags de cada sentença
    qtd_tags = []
    for token_tag in df['formato_bio']:
        for token, tag in token_tag:
            qtd_tags.append(tag)

    # 2. Contar as ocorrências de cada tag
    contagem_tags = Counter(qtd_tags)
    total_tokens = len(qtd_tags)

    # 3. Criar e exportar o DataFrame de cálculo
    df_calculo = pd.DataFrame({
        'Tipo': ['Total de Tokens', 'Tokens B-WRONG', 'Tokens I-WRONG', 'Tokens O'],
        'Quantidade': [
            total_tokens,
            contagem_tags.get('B-WRONG', 0),
            contagem_tags.get('I-WRONG', 0),
            contagem_tags.get('O', 0) ]
    })

    return df_calculo

def main():
    # Leitura do arquivo CSV (TSV), com suporte de acentuação
    try:
        leitura = pd.read_csv('resultado_extrair_sentenca_erro_semerro.tsv', encoding='latin-1', sep='\t')
    except FileNotFoundError:
        print ("Erro na leitura do arquivo 'resultado_extrair_sentenca_erro_semerro.tsv'.")
        return

    # Aplica a transformação BIO em todas as linhas
    leitura['formato_bio'] = leitura['Texto'].apply(tag2bio)

    # Coluna temporária p/ identificar duplicações
    leitura['formato_bio_str'] = leitura['formato_bio'].astype(str)

    # Criação de um Dataframe com sentenças não repetidas
    df_unico = leitura[['Texto', 'formato_bio', 'formato_bio_str']].drop_duplicates(
        subset=['Texto', 'formato_bio_str']
    ).drop(columns=['formato_bio_str']).reset_index(drop=True)

    print("*** SENTENÇAS EM FORMATO BIO *** ")

    for i in range(len(df_unico)):
        print(f"\n--- Sentença Nº{i + 1} ---")
        print(f"Sentença original: {df_unico['Texto'].iloc[i]}")
        print(f"Formato BIO: {df_unico['formato_bio'].iloc[i]}")

    # ********** Cálculo da quantidade total de tags e dos tokens B, I e O. **********

    df_calculo = calcular_estatistica_bio (df_unico)

    estatistica_tokens = 'estatistica_tokens.tsv'
    df_calculo.to_csv(estatistica_tokens, sep='\t', index=False, encoding='utf-8')

    print(f"\n*** ESTATÍSTICA DOS DADOS ***")
    print(df_calculo)

    # ********** ESTRATIFICAÇÃO DOS DADOS **********
    # 1. Cria a coluna dos rótulos BIO
    df_unico['contem_erro'] = df_unico['formato_bio'].apply(contem_erro)

    # 2. Faz a divisão nos DataFrames (df_unico), que contêm a frase original e o formato BIO
    df_train, df_test = train_test_split(df_unico,test_size=0.2,random_state=SEED,stratify = df_unico['contem_erro'])

    # 1. Tamanho dos conjuntos de dados (número de frases)
    print(f"\nTotal de frases: {len(df_unico)}")
    print(f"Frases para treinamento (80%): {len(df_train)}")
    print(f"Frases para teste (20%): {len(df_test)}")

    # Arquivos train.tsv (80%) e test.tsv (20%) com texto e contem_erro
    treino_dados = 'train.tsv'
    df_train[['Texto', 'contem_erro']].to_csv(treino_dados, sep='\t', index=False, encoding='utf-8')
    teste_dados = 'test.tsv'
    df_test[['Texto', 'contem_erro']].to_csv(teste_dados, sep='\t', index=False, encoding='utf-8')

    print("\nOs arquivos train.tsv e test.tsv foram gerados com sucesso.")

    # Arquivos train_bio.tsv (80%0 e test_bio.tsv (20%) com texto, formato_bio e contem_erro
    treino_bio_dados = 'train_bio.tsv'
    df_train[['Texto','formato_bio','contem_erro']].to_csv(treino_bio_dados, sep='\t', index=False, encoding='utf-8')
    teste_bio_dados = 'test_bio.tsv'
    df_test[['Texto','formato_bio','contem_erro']].to_csv(teste_bio_dados, sep='\t', index=False, encoding='utf-8')

    print("Os arquivos train_bio.tsv e test_bio.tsv foram gerados com sucesso.")

if __name__ == "__main__":
    main()