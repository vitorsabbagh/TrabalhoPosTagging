
import logging
import unidecode
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
# import pprint
import csv
import json
import math
import nltk
# from nltk import FreqDist
# nltk.download('punkt')
from configparser import ConfigParser

p = print

logging.basicConfig(filename='buscador.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Iniciando Avaliação do Método de Busca')
p('***Avaliação do Método de Busca***')

logging.info('Iniciando leitura do arquivo de configuração')
config = ConfigParser()
config.read('./cfg/evaluation.cfg')


logging.info('Iniciando processamento do modelo')


config.read('./cfg/general.cfg')
STEMMER = eval(config['general']['STEMMER'])
filename = './result/resultados-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1.csv'

results_query_i_docnumber = {}
with open(filename, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, result in enumerate(csvreader):
        query_number = int(result[0])
        rank_position, doc_number, similarity = eval(result[1])
        if query_number in results_query_i_docnumber:
            results_query_i_docnumber[query_number].append(doc_number)
        else:
            results_query_i_docnumber[query_number] = [doc_number]
# p(str(index) + ': ' + str(query_number) + ': ' +
#   str(rank_position) + ' ' + str(doc_number) + ' ' + str(similarity))

expected_results_query_i_docnumber = {}
with open(config['evaluation']['RESULTADOS_ESPERADOS'], newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, result in enumerate(csvreader):
        if index > 0:
            query_number = int(result[0])
            doc_number = int(result[1])
            score = int(result[2])
            if score > 4:
                if query_number in expected_results_query_i_docnumber:
                    expected_results_query_i_docnumber[query_number].append(
                        doc_number)
                else:
                    expected_results_query_i_docnumber[query_number] = [
                        doc_number]
# p(expected_results_query_i_docnumber)

precision_at_query_k_recall_i = {}
for index_query, query_number in enumerate(results_query_i_docnumber):
    if query_number in expected_results_query_i_docnumber:
        count_total_expected = len(
            expected_results_query_i_docnumber[query_number])
        A = len(set(results_query_i_docnumber[query_number]) & set(
            expected_results_query_i_docnumber[query_number]))
        count_expected = 0
        count_not_expected = 0
        precision_at_query_k_recall_i[query_number] = {}

        for index_doc, doc_number in enumerate(results_query_i_docnumber[query_number]):
            if doc_number in expected_results_query_i_docnumber[query_number]:
                count_expected += 1
            else:
                count_not_expected += 1
            precision = count_expected / (index_doc + 1)
            recall = count_expected / count_total_expected

            if recall in precision_at_query_k_recall_i[query_number]:
                precision_at_query_k_recall_i[query_number][recall] = max(
                    precision, precision_at_query_k_recall_i[query_number][recall])
            else:
                precision_at_query_k_recall_i[query_number][recall] = precision
            # p(precision_at_query_k_recall_i[query_number])
            # p(str(recall) + ' : ' + str(precision))
            if recall == 1:
                break


import pprint
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(precision_at_query_k_recall_i[query_number])


# with open('PR4.json', 'w') as file:
#     file.write(json.dumps(
#         precision_at_query_k_recall_i, indent=4))
Pi = {}
for query_number in precision_at_query_k_recall_i:
    Pi[query_number] = {}
    max_recall = max(
        precision_at_query_k_recall_i[query_number].keys())
    Pi[query_number][1] = precision_at_query_k_recall_i[query_number][max_recall]
# pp.pprint(Pi)

recall_range = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]
for query_number in precision_at_query_k_recall_i:
    for recall_wall in recall_range:
        # recall_r = 1
        max_precision = 0
        sliced_dict = {
            k: v for k, v in precision_at_query_k_recall_i[query_number].items() if k >= recall_wall}
        if len(sliced_dict) > 0:
            max_precision = max(sliced_dict.values())
        max_precision = max(max_precision, Pi[query_number][1])
        # while recall_r >= recall_wall:
        #     max_precision = max(
        #         max_precision, precision_at_query_k_recall_i[query_number][recall_r])
        Pi[query_number][round(recall_wall, 1)] = max_precision
        # recall_r -= 0.2
        # max_precision = 0

        # Pi[query_number][recall] = max(
        # precision_at_query_k_recall_i[query_number][1:recall].values())
        # recall_range_a_direita = [i for i in recall_range if i >= recall]

# pp.pprint(Pi)

average_precision = {}
precision_sum = 0
first_query = list(Pi.keys())[0]
# [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]

filename = './avalia/11pontos-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1.csv'
with open(filename, 'w') as fp:
    for recall_r, v in Pi[first_query].items():
        for query_number in Pi:
            precision_sum += Pi[query_number][recall_r]
        average_precision[recall_r] = precision_sum / len(Pi)
        precision_sum = 0
        fp.write("%2.2f, %2.2f\n" % (recall_r, average_precision[recall_r]))
# pp.pprint(average_precision)


filename = './avalia/11pontos-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1.pdf'
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
with PdfPages(filename) as export_pdf:
    lists = sorted(average_precision.items())
    x, y = zip(*lists)  # unpack a list of pairs into two tuples
    plt.plot(x, y, color='red', marker='o')
    plt.title('Precision Vs Recall', fontsize=14)
    plt.xlabel('Recall', fontsize=14)
    plt.ylabel('Precision', fontsize=14)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True)
    # plt.show()
    export_pdf.savefig()
    plt.close()


# from pandas import DataFrame
# import matplotlib.pyplot as plt
# Data2 = {'Year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
#          'Unemployment_Rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
#          }
# df2 = DataFrame(Data2, columns=['Year', 'Unemployment_Rate'])
# plt.plot(df2['Year'], df2['Unemployment_Rate'], color='red', marker='o')
# plt.title('Unemployment Rate Vs Year', fontsize=14)
# plt.xlabel('Year', fontsize=14)
# plt.ylabel('Unemployment Rate', fontsize=14)
# plt.grid(True)
# plt.show()
