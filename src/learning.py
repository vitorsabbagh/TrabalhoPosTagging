

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
    recover_w = recover_t.get(w[-2:], 0) + 1
    recover_t[w[-2:]] = recover_w
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
                    if len(word) >= 4:
                        register_sufix(tag, word.lower(), ten_fold_index)
                    last_tag = tag
            line_index += 1


if __name__ == "__main__":

    for ten_fold_index_i in range(0, 10):
        # separate_and_learn(r"./data/corpusdidactic.txt", ten_fold_index_i)
        separate_and_learn(r"./data/corpus100.txt", ten_fold_index_i)

    import pprint
    import json
    pp = pprint.PrettyPrinter(indent=4)

    with open('temp/hmm_learning_transitions.json', 'w') as file:
        file.write(json.dumps(
            {'trans': trans}, indent=4))
    with open('temp/hmm_learning_emissions.json', 'w') as file:
        file.write(json.dumps(
            {'emissions': emissions, }, indent=4))
    with open('temp/hmm_learning_sufixes.json', 'w') as file:
        file.write(json.dumps(
            {'sufixes': sufixes, }, indent=4))
    with open('temp/hmm_learning_apriori.json', 'w') as file:
        file.write(json.dumps(
            {'apriori': apriori}, indent=4))
    with open('temp/hmm_testing_data.json', mode='w', encoding="utf8") as file:
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
