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

print('\nquery: ', end='')
print(*query)

tokens = []
for i in range(len(docs)):
    tokens += nltk.word_tokenize(docs[i].lower())

# fdist = FreqDist(word.lower() for word in tokens)
# for i in fdist1 :
#     print(i)
# FreqDist(word.lower() for word in tokens).pprint()

tokens = set(tokens)

tokens = sorted(tokens)

# tokens
#
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
