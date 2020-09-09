
from bimt_viterby import Decoder
# import pprint
import json
import numpy as np
p = print
# ten_fold_index = 2

with open('temp/hmm_learning_apriori.json') as json_file:
    json_file = json.load(json_file)
    apriori_dict = json_file['apriori']

with open('temp/hmm_learning_emissions.json') as json_file:
    json_file = json.load(json_file)
    emissions = json_file['emissions']

with open('temp/hmm_learning_transitions.json') as json_file:
    json_file = json.load(json_file)
    transitions = json_file['trans']

with open('temp/hmm_testing_data.json') as json_file:
    json_file = json.load(json_file)
    testing_data = json_file['testing_data']

with open('temp/hmm_learning_sufixes.json') as json_file:
    json_file = json.load(json_file)
    sufixes = json_file['sufixes']

accuracy = {}


def register_accuracy(correct_tag, decoded_tag):
    # accuracy[correct_tag]['total'] = apriori.get(t, 0) + 1
    # if correct_tag == decoded_tag:
    #     accuracy[correct_tag]['correct'] = apriori.get(t, 0) + 1

    recover_tag = accuracy.get(correct_tag, {})
    recover_total = recover_tag.get('total', 0) + 1
    recover_tag['total'] = recover_total
    if correct_tag == decoded_tag:
        recover_correct = recover_tag.get('correct', 0) + 1
        recover_tag['correct'] = recover_correct
    accuracy[correct_tag] = recover_tag
    pass


# def unknown_words_prob(unknown_word, tag, ten_fold_index):

#     sufix = unknown_word[-2:]
    # if unknown_word[-2:]


def decode_ten_fold(ten_fold_index):

    wordset = []
    for tag in emissions[str(ten_fold_index)]:
        for word in emissions[str(ten_fold_index)][tag]:
            if not word.lower() in wordset:
                wordset.append(word.lower())
    wordset.append("PalavraDesconhecida")

    sufixset = []
    for tag in sufixes[str(ten_fold_index)]:
        for word in sufixes[str(ten_fold_index)][tag]:
            if not word.lower() in sufixset:
                sufixset.append(word.lower())

    # sentence = list(("Antes_LPREP de_LPREP iniciarmos_VTD o_ART estudo_N da_PREP+ART origem_N da_PREP+ART vida_N ,_, é_VLIG necessário_ADJ conhecer_VTD alguns_ADJ caracteres_N que_PR distinguem_VBI os_ART seres_N vivos_ADJ dos_PREP+ART seres_N brutos_ADJ ._.").split(" "))
    # sentence = list(("Antes_LPREP de_LPREP o_ART estudo_N da_PREP+ART origem_N da_PREP+ART vida_N ,_, é_VLIG necessário_ADJ conhecer_VTD alguns_ADJ caracteres_N que_PR os_ART seres_N vivos_ADJ dos_PREP+ART seres_N brutos_ADJ ._.").split(" "))

    unknown_words = []
    for sentence in testing_data[str(ten_fold_index)]:
        sentence_words = []
        sentence_tags = []
        for pair in sentence.split():
            sentence_words.append(pair.split("_")[0])
            sentence_tags.append(pair.split("_")[1])
        # text_index_list = []
        for token in sentence_words:
            if token.lower() not in wordset:
                #     text_index_list.append(wordset.index(token.lower()))
                # else:
                unknown_words.append(token.lower())
                # token =
                # text_index_list.append(wordset.index("brasil"))

    with open('hmm_unknown_words.txt', mode='a', encoding="utf8") as file:
        file.writelines("%s\n" % word for word in unknown_words)

    tagset = list(apriori_dict[str(ten_fold_index)].keys())

    N = len(tagset)

    matrix_A = np.zeros((N, N))
    # p('**matrix_A**')

    # for i in range(0, N):
    #     previous_tag = tagset[i]
    #     p(previous_tag, end=' ')
    # p()
    # for j in range(0, N):
    #     tag = tagset[j]
    #     p(tag)

    for i in range(0, N):
        previous_tag = tagset[i]
        # p("%10s   " % previous_tag, end='  ')
        for j in range(0, N):
            tag = tagset[j]
            if not previous_tag in transitions[str(ten_fold_index)]:
                matrix_A[i][j] = 0
            elif not tag in transitions[str(ten_fold_index)][previous_tag]:
                matrix_A[i][j] = 0
            else:
                transition_value = transitions[str(
                    ten_fold_index)][previous_tag][tag]
                apriori_value = apriori_dict[str(ten_fold_index)][previous_tag]
                matrix_A[i][j] = transitions[str(ten_fold_index)][previous_tag][tag] / \
                    apriori_dict[str(ten_fold_index)][previous_tag]
                pass
        #     p(matrix_A[i][j], end='  ')
        # p()

    tags_sum = 0
    for tag in tagset:
        tags_sum += apriori_dict[str(ten_fold_index)][tag]

    matrix_pi = np.zeros(N)
    for i in range(0, N):
        tag = tagset[i]
        if tag in apriori_dict[str(ten_fold_index)]:
            matrix_pi[i] = apriori_dict[str(ten_fold_index)][tag] / tags_sum
        else:
            matrix_pi[i] = 0

    matrix_pi = np.array([matrix_pi])

    # with open('hmm_words.txt', mode='w', encoding="utf8") as file:
    #     file.writelines("%s\n" % word for word in wordset)

    matrix_B = np.zeros((N, len(wordset)))
    # p('\n\n**matrix_B**')
    # for j in range(0, len(wordset)):
    #     p(wordset[j], end=' ')
    # p()

    for i in range(0, N):
        tag = tagset[i]
        # p("\n%10s   " % tag, end='  ')
        for j in range(0, len(wordset)):
            word = wordset[j].lower()
            if not tag in emissions[str(ten_fold_index)]:
                matrix_B[i][j] = 0
            elif word in emissions[str(ten_fold_index)][tag]:
                matrix_B[i][j] = emissions[str(
                    ten_fold_index)][tag][word] / apriori_dict[str(ten_fold_index)][tag]
            # elif word in unknown_words:
            #     matrix_B[i][j] = 1
            # p(matrix_B[i][j], end='  ')

    matrix_B_Sufix = np.zeros((N, len(wordset)))
    for i in range(0, N):
        tag = tagset[i]
        # p("\n%10s   " % tag, end='  ')
        for j in range(0, len(sufixset)):
            word = sufixset[j].lower()
            if not tag in sufixes[str(ten_fold_index)]:
                matrix_B_Sufix[i][j] = 0
            elif word in sufixes[str(ten_fold_index)][tag]:
                matrix_B_Sufix[i][j] = sufixes[str(
                    ten_fold_index)][tag][word] / apriori_dict[str(ten_fold_index)][tag]
            # p(matrix_B_Sufix[i][j], end='  ')
    # initialize
    decoder = Decoder(matrix_pi.T, matrix_A, matrix_B, matrix_B_Sufix)
    # p('matrix_pi.T')
    # p(matrix_pi.T)
    # p()
    # p('matrix_A')
    # p(matrix_A)
    # p()
    # p('matrix_B')
    # p(matrix_B)
    # p()
    # p('matrix_B_Sufix')
    # p(matrix_B_Sufix)
    # p()

    # data = [0, 1, 2, 3, 4]

    text_index_list = []
    unknown_words = []
    qty_testing_sentences = len(testing_data[str(ten_fold_index)])
    index_testing_sentences = 0

    for sentence in testing_data[str(ten_fold_index)]:
        index_testing_sentences += 1
        sentence_words = []
        sentence_tags = []
        text_index_list = []
        sufix_index_list = []
        for pair in sentence.split():
            # if pair.split("_")[0] == pair.split("_")[1]:
            #     continue
            sentence_words.append(pair.split("_")[0])
            sentence_tags.append(pair.split("_")[1])
        for token in sentence_words:
            # if token not in apriori_dict[str(ten_fold_index_i)]:
            if token.lower() in wordset:
                text_index_list.append(wordset.index(token.lower()))
                # p(token.lower())
            else:
                # text_index_list.append(wordset.index("estudo"))
                text_index_list.append(wordset.index("PalavraDesconhecida"))
                # p(token.lower() + '-> estudo')
            if len(token) >= 4:
                if token[-2:] in sufixset:
                    sufix_index_list.append(sufixset.index(token[-2:].lower()))
                else:
                    sufix_index_list.append(0)
            else:
                sufix_index_list.append(0)

        # p('text_index_list')
        # p(text_index_list)
        # p()
        # p('sentence_words')
        # p(sentence_words)
        # p()
        tags_decoded = decoder.Decode(
            text_index_list, sentence_words, sufix_index_list)

        i = 0
        for tag in sentence_tags:
            # p("%29s   " % str(sentence_words[i]), end='')
            # p("%10s   " % str(sentence_tags[i]), end='')
            # p("%10s   " % str(tagset[tags_decoded[i]]))
            register_accuracy(sentence_tags[i], tagset[tags_decoded[i]])
            i += 1
        # p()

        # del decoder

    p(' sentence ' + str(index_testing_sentences) +
        ' of ' + str(qty_testing_sentences))
    # p()
# print(sentence_words)
# print(tags_real)
# print(tags_decoded)


with open('hmm_unknown_words.txt', mode='w', encoding="utf8") as file:
    file.write("")

for ten_fold_index_i in range(0, 10):
    p('***ten_fold_index_i*** ' + str(ten_fold_index_i))
    decode_ten_fold(ten_fold_index_i)
    # p('\n\n\n')

# import re
sum_total = 0
sum_correct = 0
acc_total = 0
# for tag, value in accuracy.items():
for tag in accuracy:
    # if re.search('[a-zA-Z]', tag):
    if 'correct' in accuracy[tag]:
        accuracy[tag]['acc'] = accuracy[tag]['correct'] / \
            accuracy[tag]['total'] * 100
    else:
        accuracy[tag]['acc'] = 0

    if 'correct' in accuracy[tag]:
        sum_correct += accuracy[tag]['correct']
    if 'total' in accuracy[tag]:
        sum_total += accuracy[tag]['total']
acc_total = sum_correct / sum_total * 100

with open('./hmm_relatorio.txt', mode='w') as file:
    file.write('Taxa de acerto geral: %.2f%% \n' % acc_total)
    file.write('Qtde de tags processadas: %i \n' % sum_total)
    file.write('Qtde de tags processadas corretamente: %i \n\n' % sum_correct)
    for tag in accuracy:
        # for tag, v in accuracy.items():
        # if re.search('[a-zA-Z]', tag):
        file.write('Taxa de acerto da classe ' + tag + '\n')
        file.write('%s: %.2f%% \n' % (tag, accuracy[tag]['acc']))
        file.write('Total da classe: %.2f%%\n\n' % accuracy[tag]['acc'])

with open('temp/hmm_accuracy.json', mode='w', encoding="utf8") as file:
    file.write(json.dumps({'accuracy': accuracy}, indent=4))


pass
# sys.exit()
