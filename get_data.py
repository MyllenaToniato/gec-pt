import pandas as pd
import re
from collections import Counter
from sklearn.model_selection import train_test_split
import sklearn_crfsuite
from sklearn_crfsuite import metrics
from sklearn.metrics import accuracy_score

# Semente fixa (SEED) para garantir a reprodutibilidade da divisão
SEED = 100


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
        elif token == "<correct>" or token == "</correct>":
            continue  # Ignora tags correct
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


# --- FUNÇÃO AUXILIAR PARA ESTRATIFICAÇÃO ---
def frase_contem_erro(sentenca_bio):
    """Verifica se a frase contém qualquer tag de erro (WRONG)."""
    for _, tag in sentenca_bio:
        if 'WRONG' in tag:
            return True
    return False


# --- FUNÇÃO AUXILIAR PARA FEATURE ENGINEERING (CRF) ---
def extrai_caracteristicas_rotulos(df):
    X_out = []
    y_out = []
    for sentenca_bio in df['formato_bio']:
        sent_features = []
        sent_rotulos = []

        for i, (palavra, rotulo) in enumerate(sentenca_bio):
            # Feature Engineering: Extrai características contextuais
            features = {
                'word.lower()': palavra.lower(),
                'word.isupper()': palavra.isupper(),
                'word.istitle()': palavra.istitle(),
                'word.isdigit()': palavra.isdigit(),
                'bias': 1.0,
            }
            # Palavra anterior (-1)
            if i > 0:
                features.update({
                    '-1:palavra.lower()': sentenca_bio[i - 1][0].lower(),
                    '-1:palavra.istitle()': sentenca_bio[i - 1][0].istitle(),
                })
            else:
                features['BOS'] = True  # Indica o início da sentença

            # Próxima palavra (+1)
            if i < len(sentenca_bio) - 1:
                features.update({
                    '+1:palavra.lower()': sentenca_bio[i + 1][0].lower(),
                    '+1:palavra.istitle()': sentenca_bio[i + 1][0].istitle(),
                })
            else:
                features['EOS'] = True  # Indica o fim da sentença

            sent_features.append(features)
            sent_rotulos.append(rotulo)

        X_out.append(sent_features)
        y_out.append(sent_rotulos)

    return X_out, y_out


def main():
    # Caminho do arquivo (Mantido o caminho absoluto para evitar FileNotFoundError)
    caminho_file = 'C:/Users/Mylenna/PycharmProjects/gec-pt/erros_wrong_correct_com_frase_original.tsv'

    try:
        leitura = pd.read_csv(caminho_file, encoding='utf-8', sep='\t')
    except FileNotFoundError:
        print(f"\n*** ERRO: Arquivo '{caminho_file}' não encontrado. Verifique o caminho. ***")
        return

    # Aplica a transformação BIO e cria o DataFrame único
    leitura['formato_bio'] = leitura['frase_original'].apply(tag2bio)
    leitura['formato_bio_str'] = leitura['formato_bio'].astype(str)
    df_unico = leitura[['frase_original', 'formato_bio', 'formato_bio_str']].drop_duplicates(
        subset=['frase_original', 'formato_bio_str']
    ).drop(columns=['formato_bio_str']).reset_index(drop=True)

    # ... (Cálculo da estatística dos tokens e prints) ...
    print("*** SENTENÇAS EM FORMATO BIO *** ")
    for i in range(min(1, len(df_unico))):                                                          #for i in range(len(df_unico)):
        print(f"\n--- Sentença Nº{i + 1} ---")
        print(f"Sentença original: {df_unico['frase_original'].iloc[i]}")
        print(f"Formato BIO: {df_unico['formato_bio'].iloc[i]}")

    qtd_tags = []
    for token_tag in df_unico['formato_bio']:
        for token, tag in token_tag:
            qtd_tags.append(tag)

    contagem_tags = Counter(qtd_tags)
    total_tokens = len(qtd_tags)

    df_calculo = pd.DataFrame({
        'Tipo': ['Total de Tokens', 'Tokens B-WRONG', 'Tokens I-WRONG', 'Tokens O'],
        'Quantidade': [
            total_tokens,
            contagem_tags.get('B-WRONG', 0),
            contagem_tags.get('I-WRONG', 0),
            contagem_tags.get('O', 0)]
    })

    estatistica_tokens = 'estatistica_tokens.tsv'
    df_calculo.to_csv(estatistica_tokens, sep='\t', index=False, encoding='utf-8')

    print(f"\n*** ESTATÍSTICA DOS DADOS ***")
    print(df_calculo)
    print(f"\nO cálculo dos tokens foi salvo no arquivo {estatistica_tokens}")

    # ********** DIVISÃO DOS DADOS COM SCIKIT-LEARN **********

    print(f" \n*** DIVISÃO ESTRATIFICADA DOS DADOS (80% Treino, 20% Teste, SEED={SEED}) ***")

    # Criação da variável para estratificação (garante que a proporção de erros seja mantida)
    df_unico['contem_erro'] = df_unico['formato_bio'].apply(frase_contem_erro)

    # Divisão estratificada
    df_train, df_test = train_test_split(
        df_unico,
        test_size=0.2,
        random_state=SEED,
        stratify=df_unico['contem_erro']
    )

    # ********** Preparação final dos dados (Feature Engineering) **********

    X_train, y_train = extrai_caracteristicas_rotulos(df_train)
    X_test, y_test = extrai_caracteristicas_rotulos(df_test)

    print(f"Sentenças para Treinamento: {len(X_train)}")
    print(f"Sentenças para Teste: {len(X_test)}")

    # ********** Treinamento do Modelo CRF **********

    print("TREINAMENTO E AVALIAÇÃO DO MODELO CRF")


    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )

    try:
        crf.fit(X_train, y_train)
        print("\n*** Treinamento do CRF concluído com sucesso! ***")
    except AttributeError:
        print("\n*** ERRO: Falha no treinamento do CRF. ***")
        return

    # Predição e Avaliação
    y_pred = crf.predict(X_test)

    labels = list(crf.classes_)
    if 'O' in labels:
        labels.remove('O')

    print("\nRelatório de Classificação Detalhado (Foco nas tags de Erro):")
    print(metrics.flat_classification_report(
        y_test, y_pred, labels=labels, digits=4
    ))

    y_test_flat = [tag for sent in y_test for tag in sent]
    y_pred_flat = [tag for sent in y_pred for tag in sent]
    accuracy = accuracy_score(y_test_flat, y_pred_flat)
    print(f"Acurácia Geral do Token: {accuracy:.4f}\n")


if __name__ == "__main__":
    main()