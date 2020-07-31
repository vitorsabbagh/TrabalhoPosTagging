
import logging
import unidecode
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pprint
import csv
import json
from sys import exit
import math
import nltk
from nltk import FreqDist
from configparser import ConfigParser
nltk.download('punkt')


logging.basicConfig(filename='buscador.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Iniciando Módulo de Busca')


stop_words = set(stopwords.words('english'))

p = print
config = ConfigParser()
logging.info('Iniciando leitura do arquivo de configuração')
config.read('./cfg/busca.cfg')


W_Di = {}
IDFi = {}
Docs = {}
logging.info('Iniciando leitura do modelo')
with open(config['busca']['MODELO']) as json_file:
    modelo = json.load(json_file)
    W_Di = modelo['Wi']
    IDFi = modelo['IDFi']
    Docs = modelo['Docs']

distancia_Di = {}
for doc_number in Docs:
    distancia_Di[doc_number] = 0
for terms, doc_numbers in W_Di.items():
    for doc_number, weight in doc_numbers.items():
        distancia_Di[int(doc_number)] += int(weight)**2
for doc_number in distancia_Di:
    distancia_Di[doc_number] = math.sqrt(distancia_Di[doc_number])
# p(distancia_Di)

# consultas = {}
W_Qi = {}
produto_escalar_Q_Di = {}
distancia_Qi = {}
Coseno_Qi_Di = {}
logging.info('Iniciando processamento do modelo')
with open(config['busca']['CONSULTAS'], newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for query in csvreader:
        query_number = int(query[0])

        query_sentence = query[1].replace('?', '').replace(
            '\'', '').replace('(', '').replace(')', '')

        tokenizer = RegexpTokenizer(r'\w+')
        query_terms = nltk.word_tokenize(unidecode.unidecode(query_sentence))
        # remove words smaller then 3 chars
        query_terms = [f for f in query_terms if len(f) > 2]
        # remove words with numbers
        query_terms = [x for x in query_terms if not any(
            c.isdigit() for c in x)]
        query_terms = [w for w in query_terms if not w.lower() in stop_words]

        W_Qi[query_number] = {}
        # consultas[query_number] = {}
        produto_escalar_Q_Di[query_number] = {}
        distancia_Qi[query_number] = {}
        aux_distancia_Q = 0
        for query_term in query_terms:
            if query_term in IDFi:
                W_Qi[query_number][query_term] = IDFi[query_term]*1
                # for doc_number in Docs:
                # for doc_number in W_Di[query_term]:
                #     aux_produto_escalar += W_Qi[query_number][query_term] * \
                #         W_Di[query_term][doc_number]
                aux_distancia_Q += W_Qi[query_number][query_term]**2
        distancia_Qi[query_number] = math.sqrt(aux_distancia_Q)

        Coseno_Qi_Di[query_number] = {}
        for doc_number in Docs:
            aux_produto_escalar = 0
            for query_term in query_terms:
                if query_term in W_Di:
                    if str(doc_number) in W_Di[query_term]:
                        aux_produto_escalar += W_Qi[query_number][query_term] * \
                            W_Di[query_term][str(doc_number)]
            produto_escalar_Q_Di[query_number][doc_number] = aux_produto_escalar
            if distancia_Di[doc_number] > 0:
                Coseno_Qi_Di[query_number][doc_number] = produto_escalar_Q_Di[query_number][doc_number] / \
                    distancia_Qi[query_number]/distancia_Di[doc_number]

logging.info('Finalizado processamento do modelo')
# pprint.pprint(Coseno_Qi_Di)

position = 0
with open(config['busca']['RESULTADOS'], 'w') as fp:
    for query_number, ranking in Coseno_Qi_Di.items():
        sorted_ranking = sorted(
            Coseno_Qi_Di[query_number].items(), key=lambda x: x[1], reverse=True)
        position = 0
        for doc_number, coseno in sorted_ranking:
            if coseno > 0.10:
                position += 1
                fp.write("%5d; [ %2d, %5d, %2.2f]\n" %
                         (query_number, position, doc_number, coseno))


logging.info('Finalizada gravação dos resultados')


# docs = [0]*3  # Vetor de Documentos
# docs[0] = "Shipment of gold damaged in a fire"
# docs[1] = "Delivery of silver arrived in a silver truck"
# docs[2] = "Shipment of gold arrived in a truck"
# print(docs)
# # Define os termos
# query = ["gold",
#          "silver",
#          "truck"
#          ]
# query.sort()
# print('\nquery: ', end='')
# print(*query)


# tokens = []
# for i in range(len(docs)):
#     tokens += nltk.word_tokenize(docs[i].lower())
# # fdist = FreqDist(word.lower() for word in tokens)
# # for i in fdist1 :
# #     print(i)
# # FreqDist(word.lower() for word in tokens).pprint()
# tokens = set(tokens)
# tokens = sorted(tokens)


# Qi = [0]*len(tokens)  # Query Termos
# for i in range(len(tokens)):
#     Qi[i] = 0
# print("\n      TERM    Qi   ")
# for token_n in range(len(tokens)):
#     for query_n in range(len(query)):
#         if tokens[token_n] in query[query_n].lower():
#             Qi[token_n] = 1
#     print("%10s  " % tokens[token_n], end='')
#     print("%5s  " % Qi[token_n], end='')
#     print()


# fdist1 = FreqDist(tokens)
# print(fdist1['a'])

# TFi_bool = [0]*len(tokens)  # Matriz Termo Documentos
# for i in range(len(tokens)):
#     TFi_bool[i] = [0]*len(docs)

# print("\n      TERM TF1 TF2 TF3   ")

# for token_n in range(len(tokens)):
#     print("%10s  " % tokens[token_n], end='')
#     for doc_n in range(len(docs)):
#         if tokens[token_n] in docs[doc_n].lower():
#             TFi_bool[token_n][doc_n] = 1
#     print("%5s  " % TFi_bool[token_n], end='')
#     print()


# TFi_counts = [0]*len(tokens)  # Matriz Termo Documentos
# for i in range(len(tokens)):
#     TFi_counts[i] = [0]*len(docs)
# print("\n      TERM TF1 TF2 TF3   ")
# for token_n in range(len(tokens)):
#     print("%10s  " % tokens[token_n], end='')
#     for doc_n in range(len(docs)):
#         if tokens[token_n] in docs[doc_n].lower():
#             TFi_counts[token_n][doc_n] = docs[doc_n].lower().count(
#                 tokens[token_n])
#     print("%5s  " % TFi_counts[token_n], end='')
#     print()


# DFi = [0]*len(tokens)  # Matriz Termo Documentos
# for token_n in range(len(tokens)):
#     DFi[token_n] = [0]*len(docs)
# print("      TERM    DFi   ")
# for token_n in range(len(tokens)):
#     # for doc_n in range(len(docs)):
#     DFi[token_n] = sum(TFi_bool[token_n])
#     print("%10s  " % tokens[token_n], end='')
#     print("%5s  " % DFi[token_n], end='')
#     print()


# IDFi = [0]*len(tokens)  # Matriz Termo Documentos
# for token_n in range(len(tokens)):
#     IDFi[token_n] = [0]*len(docs)
# print("\n      TERM    IDFi   ")
# for token_n in range(len(tokens)):
#     IDFi[token_n] = math.log(len(docs)/DFi[token_n], 10)
#     print("%10s  " % tokens[token_n], end='')
#     print("%5s  " % IDFi[token_n], end='')
#     print()


# W_Qi = [0]*len(tokens)  # Matriz Termo Documentos
# for token_n in range(len(tokens)):
#     W_Qi[token_n] = [0]*len(docs)
# print("\n     Query W_Q1")
# for token_n in range(len(tokens)):
#     print("%10s  " % tokens[token_n], end='')
#     W_Qi[token_n] = Qi[token_n]*IDFi[token_n]
#     print("%5s  " % W_Qi[token_n], end='')
#     print()


# W_Dij = [0]*len(tokens)  # Matriz Termo Documentos
# for i in range(len(tokens)):
#     W_Dij[i] = [0]*len(docs)
# print("\n      TERM  W_Di1   W_Di2   W_Di3   ")
# for token_n in range(len(tokens)):
#     print("%10s  " % tokens[token_n], end='')
#     for doc_n in range(len(docs)):
#         W_Dij[token_n][doc_n] = IDFi[token_n] * TFi_counts[token_n][doc_n]
#         print("%.4f  " % W_Dij[token_n][doc_n], end='')
#     print()


# tamanho_vetor_D = [0]*len(docs)  # Matriz Termo Documentos
# for doc_n in range(len(docs)):
#     tamanho_vetor_D[doc_n] = 0


# print("\n     Doc tamanho_vetor")
# for doc_n in range(len(docs)):
#     print("( ", end='')
#     for token_n in range(len(tokens)):
#         tamanho_vetor_D[doc_n] += W_Dij[token_n][doc_n]**2
#         print("%.4f**2 + " % W_Dij[token_n][doc_n], end='')
#     tamanho_vetor_D[doc_n] = tamanho_vetor_D[doc_n]**0.5
#     print(" )**0.5", end='')
#     print(" -> %5s  " % tamanho_vetor_D[doc_n], end='')
#     print()


# tamanho_vetor_Q = 0
# print("\nTamanho Vetor da Query: ", end='')
# print(" ( ", end='')
# for token_n in range(len(tokens)):
#     tamanho_vetor_Q += W_Qi[token_n]**2
#     print("%.4f**2 + " % W_Qi[token_n], end='')
# tamanho_vetor_Q = tamanho_vetor_Q**0.5
# print(" )**0.5", end='')
# print(" -> %5s  " % tamanho_vetor_Q, end='')
# print()


# produto_escalar_Q_Di = [0]*len(docs)  # Matriz Termo Documentos
# for doc_n in range(len(docs)):
#     produto_escalar_Q_Di[doc_n] = 0
# print("\nProduto_escalar_Q_Di:")
# for doc_n in range(len(docs)):
#     print("D%06d -> ( " % doc_n, end='')
#     for token_n in range(len(tokens)):
#         produto_escalar_Q_Di[doc_n] += W_Dij[token_n][doc_n] * W_Qi[token_n]
#         print("%.4f*%.4f + " % (W_Dij[token_n][doc_n], W_Qi[token_n]), end='')
#     print(" )", end='')
#     print(" = %5s  " % produto_escalar_Q_Di[doc_n], end='')
#     print()

# print()
# cosine_Q_Di = [0]*len(docs)  # Matriz Termo Documentos
# for doc_n in range(len(docs)):
#     cosine_Q_Di[doc_n] = 0
# for doc_n in range(len(docs)):
#     print("cosine_Q_D%d " % doc_n, end='')
#     for token_n in range(len(tokens)):
#         cosine_Q_Di[doc_n] = produto_escalar_Q_Di[doc_n] / \
#             tamanho_vetor_Q / tamanho_vetor_D[doc_n]
#         # print("%.4f*%.4f + "% (W_Dij[token_n][doc_n] , W_Qi[token_n]),end='')
#     # print(" )",end='')
#     print("= %5s  " % cosine_Q_Di[doc_n], end='')
#     print()


# # Lista invertida
# print()
# ranking = {}
# for doc_n in range(len(docs)):
#     ranking[docs[doc_n]] = cosine_Q_Di[doc_n]
# ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
# # print(ranking)

# for i in ranking:
#     print(i[0], i[1])
