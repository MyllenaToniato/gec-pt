import pandas as pd

def tag2bio(sentenca):
    # ** Eliminação dos blocos iniciais e finais dos corrects **

    # Parte 1: Encontrar as tags
    taginicial_correct = "<correct>"
    tagfinal_correct = "</correct>"

    # Parte 2: Retirá-las
    sent_temp = sentenca  # variável "sentença temporária"
    while taginicial_correct in sent_temp and tagfinal_correct in sent_temp:

        indice_inicial = sent_temp.index(taginicial_correct)  # achar a posição inicial da tag inicial do correct
        indice_inicial_tagfinal = sent_temp.index(tagfinal_correct,
                                                  indice_inicial)  # achar o índice inicial da tag final do correct
        indice_final = indice_inicial_tagfinal + len(tagfinal_correct)  # calcular a posição final do "</correct>"
        sent_temp = sent_temp[:indice_inicial] + sent_temp[
            indice_final:]  # armazenar a sentença sem as tags e o conteúdo de dentro delas

        if indice_inicial != -1 and indice_inicial_tagfinal != -1:  # remover do segmento se ambos os índices forem encontrados
            indice_final = indice_inicial_tagfinal + len(
                tagfinal_correct)  # calcular o índice final do trecho (com o </correct>)
            sent_temp = sent_temp[:indice_inicial] + sent_temp[indice_final:]  # excluir o segmento

    # ** Separação e armazenamento dos tokens **

    # Parte 1: Separação das tags
    sent_temp2 = sent_temp
    for tag in ["<wrong>", "</wrong>"]:
        sent_temp2 = sent_temp2.replace(tag, " " + tag + " ")

    # Parte 2: Separação da pontuação
    sep_pont = ['.', ',', ';', ':', '?', '!', '(', ')', '[', ']', '{', '}', "'", '"']
    for pontuacao in sep_pont:
        sent_temp2 = sent_temp2.replace(pontuacao, " " + pontuacao + " ")

    # Parte 3: Guardar tokens separados
    tokens = []
    for token in sent_temp2.split(' '):
        if token != "":
            tokens.append(token)

    # ** Transformar para tag BIO **
    bio = []
    trecho_errado = False
    primeiro_erro = True

    for token in tokens:
        if token == "<wrong>":  # se token estiver nessa tag, indica o início do erro
            trecho_errado = True
            primeiro_erro = True
        elif token == "</wrong>":  # se token estiver nessa tag, indica o término do trecho do erro
            trecho_errado = False
        else:
            if trecho_errado:  # se token estiver dentro do trecho errado
                if primeiro_erro:
                    bio.append((token, "B-WRONG"))  # adicinar B-WRONG para primeiro erro
                    primeiro_erro = False
                else:
                    bio.append((token, "I-WRONG"))  # adicinar I-WRONG para resto do trecho
            else:
                bio.append((token, "O"))  # se fora do trecho errado, adicinar O

    return bio


def main():
    # Leitura do arquivo CSV (TSV), com suporte de acentuação
    leitura = pd.read_csv('erros_wrong_correct_com_frase_original.tsv', encoding='latin-1', sep='\t')

    # Tranformação da primeira frase através da função tag2bio
    frase1 = leitura['frase_original'].iloc[0]
    formato_bio = tag2bio(frase1)

    # Output da frase
    print("*** SENTENÇA TRANSFORMADA PARA O FORMATO BIO *** ")
    print(f"Sentença original: {frase1}")
    print(f"Formato BIO: {formato_bio}")


if __name__ == "__main__":
    main()