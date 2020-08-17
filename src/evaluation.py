
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

from itertools import islice


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


p = print

logging.basicConfig(filename='buscador.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Iniciando Avaliação do Método de Busca')
logging.getLogger('matplotlib.font_manager').disabled = True

p('***Avaliação do Método de Busca***')

logging.info('Iniciando leitura do arquivo de configuração')
config = ConfigParser()
config.read('./cfg/evaluation.cfg')


logging.info('Iniciando processamento do modelo')


config.read('./cfg/general.cfg')
STEMMER = eval(config['general']['STEMMER'])
filename_stemmer = config['evaluation']['RESULTADOS_STEMMER']
filename_nostemmer = config['evaluation']['RESULTADOS_NOSTEMMER']

results_stemmer_query_i_docnumber = {}
with open(filename_stemmer, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, result in enumerate(csvreader):
        query_number = int(result[0])
        rank_position, doc_number, similarity = eval(result[1])
        if query_number in results_stemmer_query_i_docnumber:
            results_stemmer_query_i_docnumber[query_number].append(doc_number)
        else:
            results_stemmer_query_i_docnumber[query_number] = [doc_number]

results_nostemmer_query_i_docnumber = {}
with open(filename_nostemmer, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, result in enumerate(csvreader):
        query_number = int(result[0])
        rank_position, doc_number, similarity = eval(result[1])
        if query_number in results_nostemmer_query_i_docnumber:
            results_nostemmer_query_i_docnumber[query_number].append(
                doc_number)
        else:
            results_nostemmer_query_i_docnumber[query_number] = [doc_number]
# p(str(index) + ': ' + str(query_number) + ': ' +
#   str(rank_position) + ' ' + str(doc_number) + ' ' + str(similarity))

expected_query_i_docnumber = {}
with open(config['evaluation']['RESULTADOS_ESPERADOS'], newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, result in enumerate(csvreader):
        if index > 0:
            query_number = int(result[0])
            doc_number = int(result[1])
            score = int(result[2])
            if score > 4:
                if query_number in expected_query_i_docnumber:
                    expected_query_i_docnumber[query_number].append(
                        doc_number)
                else:
                    expected_query_i_docnumber[query_number] = [
                        doc_number]
# p(expected_query_i_docnumber)

if STEMMER:
    results_query_i_docnumber = results_stemmer_query_i_docnumber
else:
    results_query_i_docnumber = results_nostemmer_query_i_docnumber

precision_at_query_k_recall_i = {}
for index_query, query_number in enumerate(results_query_i_docnumber):
    if query_number in expected_query_i_docnumber:
        count_total_expected = len(
            expected_query_i_docnumber[query_number])
        A = len(set(results_query_i_docnumber[query_number]) & set(
            expected_query_i_docnumber[query_number]))
        count_expected = 0
        count_not_expected = 0
        precision_at_query_k_recall_i[query_number] = {}

        for index_doc, doc_number in enumerate(results_query_i_docnumber[query_number]):
            if doc_number in expected_query_i_docnumber[query_number]:
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
# pp.pprint(precision_at_query_k_recall_i)


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

# pp.pprint(Pi)

average_precision = {}
precision_sum = 0
first_query = list(Pi.keys())[0]

filename = './avalia/11pontos-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1.csv'

with open(filename, 'w') as fp:
    for recall_r, v in Pi[first_query].items():
        for query_number in Pi:
            precision_sum += Pi[query_number][recall_r]
        average_precision[recall_r] = precision_sum / len(Pi)
        precision_sum = 0
        fp.write("%2.2f; %2.2f\n" % (recall_r, average_precision[recall_r]))
# pp.pprint(average_precision)


filename = './avalia/11pontos-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1'
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
with PdfPages(filename + '.pdf') as export_pdf:
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
    plt.savefig(filename)
    export_pdf.savefig()
    plt.close()

Precision_at_5 = {}
Precision_at_10 = {}


for query_number, result_query_i in results_query_i_docnumber.items():
    # p('*** Query ' + str(query_number) + ' ***')
    # p('RESULT       ', end='')
    # p(results_query_i_docnumber[query_number][:10])
    # p('EXPECTED     ', end='')
    if query_number in expected_query_i_docnumber:
        # p(expected_query_i_docnumber[query_number])
        if len(result_query_i) >= 5:
            results_in_common = list(set(expected_query_i_docnumber[query_number]) & set(
                result_query_i[:5]))
            # p('IN COMMON @5 ', end='')
            # p(results_in_common)
            Precision_at_5[query_number] = len(results_in_common) / 5
            # p('Precision@5  ', end='')
            # p(str(Precision_at_5[query_number] * 100) + '%')

            if len(result_query_i) >= 10:
                results_in_common = list(set(expected_query_i_docnumber[query_number]) & set(
                    result_query_i[:10]))
                # p('IN COMMON @10', end='')
                # p(results_in_common)
                Precision_at_10[query_number] = len(results_in_common) / 10
                # p('Precision@10 ', end='')
                # p(str(Precision_at_10[query_number] * 100) + '%')


Precision_A_B = {}
for query_number, result_query_i in results_stemmer_query_i_docnumber.items():
    # p('*** Query ' + str(query_number) + ' ***')
    # p('RESULT STEMMER   ', end='')
    # p(results_stemmer_query_i_docnumber[query_number][:10])
    # p('RESULT NOSTEMMER ', end='')
    # p(results_nostemmer_query_i_docnumber[query_number][:10])
    if query_number in expected_query_i_docnumber:
        # p('EXPECTED         ', end='')
        # p(expected_query_i_docnumber[query_number])
        rel = len(expected_query_i_docnumber[query_number])

        if len(result_query_i) >= rel:

            results_in_common_stemmer = list(set(expected_query_i_docnumber[query_number]) & set(
                result_query_i[:rel]))
            # p('IN COMMON STEMMER    ', end='')
            # p(results_in_common_stemmer)

            results_in_common_nostemmer = list(set(expected_query_i_docnumber[query_number]) & set(
                results_nostemmer_query_i_docnumber[query_number][:rel]))
            # p('IN COMMON NOSTEMMER  ', end='')
            # p(results_in_common_nostemmer)

            Precision_A_B[query_number] = (
                len(results_in_common_stemmer) - len(results_in_common_nostemmer)) / rel
            # p('Precision A minus B  ', end='')
            # p('%.2f %%' % (Precision_A_B[query_number] * 100))

p('')

# pp.pprint(Precision_A_B)

# xmax = max(Precision_A_B.keys())
# ymax = max(Precision_A_B.values())
# ymin = min(Precision_A_B.values())


filename = './avalia/average_precision-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1.csv'
Average_Precision = {}
with open(filename, 'w') as fp:
    for query_number, result_query_i in results_query_i_docnumber.items():
        # p('*** Query ' + str(query_number) + ' ***')
        # p('RESULT STEMMER   ', end='')
        # p(results_stemmer_query_i_docnumber[query_number][:10])
        # p('RESULT NOSTEMMER ', end='')
        # p(results_nostemmer_query_i_docnumber[query_number][:10])
        if query_number in expected_query_i_docnumber:
            # p('EXPECTED         ', end='')
            # p(expected_query_i_docnumber[query_number])
            count_relevant = 0
            count_not_relevant = 0
            Average_Precision[query_number] = 0
            for doc_number in result_query_i:
                if doc_number in expected_query_i_docnumber[query_number]:
                    count_relevant += 1
                    Average_Precision[query_number] += count_relevant / \
                        (count_relevant + count_not_relevant)
                    # p(count_relevant / (count_relevant + count_not_relevant))
                else:
                    count_not_relevant += 1
            if count_relevant > 0:
                Average_Precision[query_number] /= count_relevant

            fp.write("%s; %2.2f\n" %
                     (query_number, Average_Precision[query_number]))
# pp.pprint(Average_Precision)

MAP = sum(Average_Precision.values()) / float(len(Average_Precision))
p('\nMAP:     %.2f' % MAP)

filename = './avalia/MAP-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1.csv'
with open(filename, 'w') as fp:
    fp.write("%s" % MAP)


# filename = './avalia/reciprocal_rank-' + \
#     ('stemmer' if STEMMER else 'nostemmer') + '-1.csv'
Reciprocal_Rank = {}
# with open(filename, 'w') as fp:
for query_number, result_query_i in results_query_i_docnumber.items():
    # p('*** Query ' + str(query_number) + ' ***')
    # p('RESULT STEMMER   ', end='')
    # p(results_stemmer_query_i_docnumber[query_number][:10])
    # p('RESULT NOSTEMMER ', end='')
    # p(results_nostemmer_query_i_docnumber[query_number][:10])
    if query_number in expected_query_i_docnumber:
        # p('EXPECTED         ', end='')
        # p(expected_query_i_docnumber[query_number])
        # if len(result_query_i) >= rel:
        position = 1
        Reciprocal_Rank[query_number] = 0
        for doc_number in result_query_i:
            if doc_number in expected_query_i_docnumber[query_number]:
                Reciprocal_Rank[query_number] = 1 / position
            else:
                position += 1
        # fp.write("%s; %s\n" %
        #          (query_number, Reciprocal_Rank[query_number]))

# pp.pprint(Reciprocal_Rank)

MRR = sum(Reciprocal_Rank.values()) / float(len(Reciprocal_Rank))
p('\nMRR:     %.2f' % MRR)


filename = './avalia/histograma_R_precision-stemmer-1.csv'
with open(filename, 'w') as fp:
    for query_number, value in Precision_A_B.items():
        fp.write("%s; %f\n" % (query_number, value))

plt.figure()
plt.bar(Precision_A_B.keys(), Precision_A_B.values())
plt.title('Histograma R-Precision')
plt.xlabel('Query Number')
plt.ylabel('RP_stemmer - RP_nostemmer')
# plt.axis([0, xmax, ymin, ymax])
# plt.show()
plt.savefig('./avalia/histograma_R_precision-stemmer-1.png')


filename = './avalia/reciprocal_rank-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1'
with open(filename + '.csv', 'w') as fp:
    for query_number, value in Reciprocal_Rank.items():
        fp.write("%s; %s\n" %
                 (query_number, value))
plt.figure()
plt.bar(Reciprocal_Rank.keys(), Reciprocal_Rank.values())
plt.title('Reciprocal_Rank')
plt.xlabel('Query Number')
plt.ylabel('')
# plt.axis([0, xmax, ymin, ymax])
# plt.show()
plt.savefig(filename)

filename = './avalia/MRR-' + \
    ('stemmer' if STEMMER else 'nostemmer') + '-1.csv'
with open(filename, 'w') as fp:
    fp.write("%s" % MRR)
