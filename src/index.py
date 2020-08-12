
import logging
from configparser import ConfigParser
import json
import pprint
import math
from sys import exit
import csv
p = print


logging.basicConfig(filename='buscador.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Iniciando Indexador de documentos')

config = ConfigParser()
logging.info('Iniciando leitura do arquivo de configuração')
config.read('./cfg/index.cfg')

logging.info('Iniciando leitura da lista invertida')
lista_invertida = {}
with open(config['index']['LEIA'], newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in csvreader:
        # print(', '.join(row))
        # print(row[0])
        # print(list(row[1].replace('[', '').replace(']', '').split(', ')))
        # IDFi.append([row[0], math.log( len(docs)/DFi[token_n], 10)] =
        lista_invertida[row[0]] = list(
            map(int, row[1].replace('[', '').replace(']', '').split(', ')))

docs = []
for key, value in lista_invertida.items():
    docs.extend(value)

docs = sorted(set(docs))
# p(docs)

logging.info('Iniciado processamento do modelo')
Wi = {}
# print(tfi)
IDFi = {}
for term, doclist in lista_invertida.items():
    IDFi[term] = math.log10(len(docs)/(len(set(lista_invertida[term]))))
    # p(str(term)+' '+str(IDFi[term]))
    # print("%29s   " % str(term), end='')
    # print("%10s   " % str(len(set(lista_invertida[term]))), end='')
    # print("%10s   " % str(IDFi[term]))

    Wi[term] = {}
    for doc in doclist:
        Wi[term][doc] = IDFi[term]*1

logging.info('Finalizado processamento do modelo')
# pprint.pprint(Wi)

with open(config['index']['ESCREVA'], 'w') as file:
    file.write(json.dumps({'Wi': Wi, 'IDFi': IDFi, 'Docs': docs}, indent=4))

logging.info('Finalizado gravação do modelo')

logging.info('\n\n')
# for term,doclist in lista_invertida.iteritems(): # the basic way
#     temp = ""
#     temp+=term
#     for k2,v2 in v1.iteritems():
#         temp = temp+" "+str(k2)+" "+str(v2)
#     print temp

# IDFi = [0]*len(tokens)  # Matriz Termo Documentos
# for token_n in range(len(tokens)):
#     IDFi[token_n] = [0]*len(docs)
# print("\n      TERM    IDFi   ")
# for token_n in range(len(tokens)):
#     IDFi[token_n] = math.log(len(docs)/DFi[token_n], 10)
#     print("%10s  " % tokens[token_n], end='')
#     print("%5s  " % IDFi[token_n], end='')
#     print()
