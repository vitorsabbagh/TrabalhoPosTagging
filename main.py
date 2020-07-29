import math
import nltk
from nltk import FreqDist
nltk.download('punkt')

docs = [0]*3  # Vetor de Documentos

docs[0] = "Shipment of gold damaged in a fire"
docs[1] = "Delivery of silver arrived in a silver truck"
docs[2] = "Shipment of gold arrived in a truck"

print(docs)

# Define os termos
query = ["gold",
         "silver",
         "truck"
         ]
query.sort()

print('query: ', end='')
print(*query)


tokens = []
for i in range(len(docs)):
    tokens += nltk.word_tokenize(docs[i].lower())
tokens = set(tokens)

tokens = sorted(tokens)

# tokens

Qi = [0]*len(tokens)  # Query Termos
for i in range(len(tokens)):
    Qi[i] = 0

print("\n      TERM    Qi   ")

for token_n in range(len(tokens)):
    for query_n in range(len(query)):
        if tokens[token_n] in query[query_n].lower():
            Qi[token_n] = 1
    print("%10s  " % tokens[token_n], end='')
    print("%5s  " % Qi[token_n], end='')
    print()

fdist1 = FreqDist(tokens)
# fdist1['a']

TFi_bool = [0]*len(tokens)  # Matriz Termo Documentos
for i in range(len(tokens)):
    TFi_bool[i] = [0]*len(docs)

print("\n      TERM TF1 TF2 TF3   ")

for token_n in range(len(tokens)):
    print("%10s  " % tokens[token_n], end='')
    for doc_n in range(len(docs)):
        if tokens[token_n] in docs[doc_n].lower():
            TFi_bool[token_n][doc_n] = 1
    print("%5s  " % TFi_bool[token_n], end='')
    print()

TFi_counts = [0]*len(tokens)  # Matriz Termo Documentos
for i in range(len(tokens)):
    TFi_counts[i] = [0]*len(docs)

print("\n      TERM TF1 TF2 TF3   ")

for token_n in range(len(tokens)):
    print("%10s  " % tokens[token_n], end='')
    for doc_n in range(len(docs)):
        if tokens[token_n] in docs[doc_n].lower():
            TFi_counts[token_n][doc_n] = docs[doc_n].lower().count(
                tokens[token_n])
    print("%5s  " % TFi_counts[token_n], end='')
    print()

DFi = [0]*len(tokens)  # Matriz Termo Documentos
for token_n in range(len(tokens)):
    DFi[token_n] = [0]*len(docs)

print("\n      TERM    DFi   ")

for token_n in range(len(tokens)):
    # for doc_n in range(len(docs)):
    DFi[token_n] = sum(TFi_bool[token_n])
    print("%10s  " % tokens[token_n], end='')
    print("%5s  " % DFi[token_n], end='')
    print()

IDFi = [0]*len(tokens)  # Matriz Termo Documentos
for token_n in range(len(tokens)):
    IDFi[token_n] = [0]*len(docs)

print("\n      TERM    IDFi   ")
for token_n in range(len(tokens)):
    IDFi[token_n] = math.log(len(docs)/DFi[token_n], 10)
    print("%10s  " % tokens[token_n], end='')
    print("%5s  " % IDFi[token_n], end='')
    print()

W_Qi = [0]*len(tokens)  # Matriz Termo Documentos
for token_n in range(len(tokens)):
    W_Qi[token_n] = [0]*len(docs)

print("\n     Query W_Q1")

for token_n in range(len(tokens)):
    print("%10s  " % tokens[token_n], end='')
    W_Qi[token_n] = Qi[token_n]*IDFi[token_n]
    print("%5s  " % W_Qi[token_n], end='')
    print()

W_Dij = [0]*len(tokens)  # Matriz Termo Documentos
for i in range(len(tokens)):
    W_Dij[i] = [0]*len(docs)

print("\n      TERM  W_Di1   W_Di2   W_Di3   ")

for token_n in range(len(tokens)):
    print("%10s  " % tokens[token_n], end='')
    for doc_n in range(len(docs)):
        W_Dij[token_n][doc_n] = IDFi[token_n] * TFi_counts[token_n][doc_n]
        print("%.4f  " % W_Dij[token_n][doc_n], end='')
    print()

tamanho_vetor_D = [0]*len(docs)  # Matriz Termo Documentos
for doc_n in range(len(docs)):
    tamanho_vetor_D[doc_n] = 0


print("\n     Doc tamanho_vetor_D")

for doc_n in range(len(docs)):

    print("( ", end='')
    for token_n in range(len(tokens)):
        tamanho_vetor_D[doc_n] += W_Dij[token_n][doc_n]**2
        print("%.4f**2 + " % W_Dij[token_n][doc_n], end='')
    tamanho_vetor_D[doc_n] = tamanho_vetor_D[doc_n]**0.5
    print(" )**0.5", end='')
    print(" -> %5s  " % tamanho_vetor_D[doc_n], end='')
    print()

tamanho_vetor_Q = 0

print("\nTamanho Vetor da Query: ", end='')

print(" ( ", end='')
for token_n in range(len(tokens)):
    tamanho_vetor_Q += W_Qi[token_n]**2
    print("%.4f**2 + " % W_Qi[token_n], end='')
tamanho_vetor_Q = tamanho_vetor_Q**0.5
print(" )**0.5", end='')
print(" -> %5s  " % tamanho_vetor_Q, end='')
print()

produto_escalar_Q_Di = [0]*len(docs)  # Matriz Termo Documentos
for doc_n in range(len(docs)):
    produto_escalar_Q_Di[doc_n] = 0


print("\nProduto_escalar_Q_Di:")

for doc_n in range(len(docs)):

    print("D%06d -> ( " % doc_n, end='')
    for token_n in range(len(tokens)):
        produto_escalar_Q_Di[doc_n] += W_Dij[token_n][doc_n] * W_Qi[token_n]
        print("%.4f*%.4f + " % (W_Dij[token_n][doc_n], W_Qi[token_n]), end='')
    print(" )", end='')
    print(" = %5s  " % produto_escalar_Q_Di[doc_n], end='')
    print()

cosine_Q_Di = [0]*len(docs)  # Matriz Termo Documentos
for doc_n in range(len(docs)):
    cosine_Q_Di[doc_n] = 0


for doc_n in range(len(docs)):
    print("cosine_Q_D%d " % doc_n, end='')
    for token_n in range(len(tokens)):
        cosine_Q_Di[doc_n] = produto_escalar_Q_Di[doc_n] / \
            tamanho_vetor_Q / tamanho_vetor_D[doc_n]
        # print("%.4f*%.4f + "% (W_Dij[token_n][doc_n] , W_Qi[token_n]),end='')
    # print(" )",end='')
    print("= %5s  " % cosine_Q_Di[doc_n], end='')
    print()

# Lista invertida
ranking = {}
for doc_n in range(len(docs)):
    ranking[docs[doc_n]] = cosine_Q_Di[doc_n]

ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
# print(ranking)

print()
print('\nRanking Final:')
for i in ranking:
    print(i[0], i[1])
