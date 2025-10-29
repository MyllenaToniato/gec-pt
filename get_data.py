import pandas as pd
import re

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


def main():
    # Leitura do arquivo CSV (TSV), com suporte de acentuação
    leitura = pd.read_csv('erros_wrong_correct_com_frase_original.tsv', encoding='utf-8', sep='\t')

    # Aplica a transformação BIO em todas as linhas
    leitura['formato_bio'] = leitura['frase_original'].apply(tag2bio)

    # Coluna temporária
    leitura['formato_bio_str'] = leitura['formato_bio'].astype(str)

    # Criação de um Dataframe com sentenças não repetidas
    df_unico = leitura[['frase_original', 'formato_bio', 'formato_bio_str']].drop_duplicates(
        subset=['frase_original', 'formato_bio_str']
    ).drop(columns=['formato_bio_str']).reset_index(drop=True)

    print("*** SENTENÇAS EM FORMATO BIO *** ")

    for i in range(len(df_unico)):
        print(f"\n--- Sentença Nº{i + 1} ---")
        print(f"Sentença original: {df_unico['frase_original'].iloc[i]}")
        print(f"Formato BIO: {df_unico['formato_bio'].iloc[i]}")

if __name__ == "__main__":
    main()