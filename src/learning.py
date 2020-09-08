

import pprint
# import csv
import json
p = print

trans = {}
emissions = {}
apriori = {}

sufixes = {}

testing_data = {}


def register_trans(tim1, ti, ten_fold_index):
    recover_tim1 = trans[ten_fold_index].get(tim1, {})
    recover_ti = recover_tim1.get(ti, 0) + 1
    recover_tim1[ti] = recover_ti
    trans[ten_fold_index][tim1] = recover_tim1


def register_emission(t, w, ten_fold_index):
    recover_t = emissions[ten_fold_index].get(t, {})
    recover_w = recover_t.get(w, 0) + 1
    recover_t[w] = recover_w
    emissions[ten_fold_index][t] = recover_t
    pass


def register_apriori(t, ten_fold_index):
    apriori[ten_fold_index][t] = apriori[ten_fold_index].get(t, 0) + 1


def register_sufix(t, w, ten_fold_index):
    recover_t = sufixes[ten_fold_index].get(t, {})
    recover_w = recover_t.get(w[-4:], 0) + 1
    recover_t[w[-4:]] = recover_w
    sufixes[ten_fold_index][t] = recover_t
    pass


# def learn_from_file(filename):
#     last_tag = "."
#     with open(filename, mode="r", encoding="utf8") as file:
#         for line in file:
#             token_list = line.split()
#             for atoken in token_list:
#                 word, tag = atoken.split("_")
#                 register_trans(last_tag, tag)
#                 register_emission(tag, word)
#                 register_apriori(tag)
#                 last_tag = tag


def separate_and_learn(filename, ten_fold_index):
    last_tag = "."
    with open(filename, mode="r", encoding="utf8") as file:
        line_index = 0
        testing_data[ten_fold_index] = []
        trans[ten_fold_index] = {}
        emissions[ten_fold_index] = {}
        sufixes[ten_fold_index] = {}
        apriori[ten_fold_index] = {}

        for line in file:
            if line_index % 10 == ten_fold_index:
                testing_data[ten_fold_index].append(line)
            else:
                token_list = line.split()
                for atoken in token_list:
                    word, tag = atoken.split("_")
                    register_trans(last_tag, tag, ten_fold_index)
                    register_emission(tag, word.lower(), ten_fold_index)
                    register_apriori(tag, ten_fold_index)
                    if len(word) > 6:
                        register_sufix(tag, word.lower(), ten_fold_index)
                    last_tag = tag
            line_index += 1


if __name__ == "__main__":

    for ten_fold_index_i in range(0, 10):
        separate_and_learn(r"./data/corpus100.txt", ten_fold_index_i)

    import pprint
    import json
    pp = pprint.PrettyPrinter(indent=4)

    with open('./hmm_learning_transitions.json', 'w') as file:
        file.write(json.dumps(
            {'trans': trans}, indent=4))
    with open('./hmm_learning_emissions.json', 'w') as file:
        file.write(json.dumps(
            {'emissions': emissions, }, indent=4))
    with open('./hmm_learning_sufixes.json', 'w') as file:
        file.write(json.dumps(
            {'sufixes': sufixes, }, indent=4))
    with open('./hmm_learning_apriori.json', 'w') as file:
        file.write(json.dumps(
            {'apriori': apriori}, indent=4))
    with open('./hmm_testing_data.json', mode='w', encoding="utf8") as file:
        file.write(json.dumps({'testing_data': testing_data}, indent=4))
    # p('***trans***')
    # pp.pprint(trans)
    # p()
    # p('***emissions***')
    # pp.pprint(emissions)
    # p()
    # p('***apriori***')
    # pp.pprint(apriori)
    # p()

"""
p('***Separação dados de aprendizado e testes***')


learning_data = []
testing_data = []

txt_data = open('./data/marcado.txt', encoding="utf8").read().split('._.')
# p(txt_data)

for index in range(len(txt_data)):
    if index % 10 == 0:
        testing_data.append(txt_data[index])
    else:
        learning_data.append(txt_data[index])
# p(testing_data)

tags_dict
for sentence_index in range(len(learning_data)):
    tags_dict
 """

"""
with open(filename) as f:
    for line in f:
        mynumbers.append([int(n) for n in line.strip().split(',')])
for pair in mynumbers:
    try:
        x, y = pair[0], pair[1]
        # Do Something with x and y
    except IndexError:
        print("A line in the file doesn't have enough entries.")


with open('./data/marcado.txt', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, result in enumerate(csvreader):
        query_number = int(result[0])
        rank_position, doc_number, similarity = eval(result[1])
        if query_number in results_stemmer_query_i_docnumber:
            results_stemmer_query_i_docnumber[query_number] += 1
        else:
            results_stemmer_query_i_docnumber[query_number] = 1

results_stemmer_query_i_docnumber = {}
with open(filename_stemmer, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for index, result in enumerate(csvreader):
        query_number = int(result[0])
        rank_position, doc_number, similarity = eval(result[1])
        if query_number in results_stemmer_query_i_docnumber:
            results_stemmer_query_i_docnumber[query_number] += 1
        else:
            results_stemmer_query_i_docnumber[query_number] = 1


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
 """
