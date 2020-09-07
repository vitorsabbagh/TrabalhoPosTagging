
import pprint
import json
import numpy as np
p = print

with open('hmm_learning_apriori.json') as json_file:
    json_file = json.load(json_file)
    apriori_dict = json_file['apriori']
    tag_list = list(apriori_dict.keys())

with open('hmm_learning_emissions.json') as json_file:
    json_file = json.load(json_file)
    emissions = json_file['emissions']

with open('hmm_learning_transitions.json') as json_file:
    json_file = json.load(json_file)
    transitions = json_file['trans']


N = len(tag_list)
matrix_A = np.zeros((N, N))

for i in range(0, N):
    previous_tag = tag_list[i]
    for j in range(0, N):
        tag = tag_list[j]
        if not previous_tag in transitions:
            matrix_A[i][j] = 0
        elif not tag in transitions[previous_tag]:
            matrix_A[i][j] = 0
        else:
            matrix_A[i][j] = transitions[previous_tag][tag] / \
                apriori_dict[previous_tag]

tags_sum = 0
for tag in tag_list:
    tags_sum += apriori_dict[tag]

matrix_pi = np.zeros(N)
for i in range(0, N):
    tag = tag_list[i]
    if tag in apriori_dict:
        matrix_pi[i] = apriori_dict[tag] / tags_sum
    else:
        matrix_pi[i] = 0

matrix_pi = np.array([matrix_pi])

words = []
for tag in emissions:
    for word in emissions[tag]:
        if not word in words:
            words.append(word)

matrix_B = np.zeros((N, len(words)))
for i in range(0, N):
    tag = tag_list[i]
    for j in range(0, len(words)):
        word = words[j]
        if not tag in emissions:
            matrix_B[i][j] = 0
        elif not word in emissions[tag]:
            matrix_B[i][j] = 0
        else:
            matrix_B[i][j] = emissions[tag][word] / apriori_dict[tag]


from bimt_viterby import Decoder


# initialize
decoder = Decoder(matrix_pi.T, matrix_A, matrix_B)


data = [0, 1, 2, 3, 4]
x = decoder.Decode(data)
print(x)

import sys
sys.exit()
