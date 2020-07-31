import pprint
from sys import exit
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import math
import unidecode
from configparser import ConfigParser
from xml.dom import minidom
import xml.etree.cElementTree as ET
import csv
import nltk
from nltk import FreqDist
nltk.download('punkt')
nltk.download('stopwords')

loop_limiter = 200000
p = print


def shave(myString):
    # tokenizer = RegexpTokenizer(r'\w+')
    # myString = tokenizer.tokenize(myString)
    myString = myString.replace('"', '').replace('\'', '').replace(';', '').replace('-', '').replace(
        '\n', ' ').replace('\r', '').replace('  ', ' ').replace('  ', ' ').replace('.', '').upper()
    # myString = myString.str.findall('\w{4,}').str.join(' ')
    myString = unidecode.unidecode(myString)
    # myString = myString.replace(r'\b(\w{1,3})\b', '')
    return myString


config = ConfigParser()
config.read('./cfg/gli.cfg')
print('\n***Gerador de Lista Invertida***')

docsXML = config['gli']['LEIA'].split(',')
# for docXML in docsXML:
# do something with path
# print('LEIA: '+docXML)

# tokens = [0]*10000
lista_invertida = {}
stop_words = set(stopwords.words('english'))
new_tokens = []
for docXML in docsXML:
    doc = minidom.parse(docXML)
    records = doc.getElementsByTagName('RECORD')
    for record in records[:loop_limiter]:
        auxDocNumber = 0
        if record.getElementsByTagName(
                'RECORDNUM'):
            auxDocNumber = int(record.getElementsByTagName(
                'RECORDNUM')[0].firstChild.data)
            if record.getElementsByTagName('ABSTRACT'):
                auxAbstract = record.getElementsByTagName('ABSTRACT')[
                    0].firstChild.data
            elif record.getElementsByTagName('EXTRACT'):
                auxAbstract = record.getElementsByTagName('EXTRACT')[
                    0].firstChild.data
            else:
                auxAbstract = record.getElementsByTagName('TITLE')[
                    0].firstChild.data
            tokenizer = RegexpTokenizer(r'\w+')
            new_tokens = nltk.word_tokenize(shave(auxAbstract))
            # remove words smaller then 3 chars
            new_tokens = [f for f in new_tokens if len(f) > 2]
            # remove words with numbers
            new_tokens = [x for x in new_tokens if not any(
                c.isdigit() for c in x)]
            new_tokens = [w for w in new_tokens if not w.lower() in stop_words]

            # tokens += tokenizer.tokenize(shave(auxAbstract))
            # lista_invertida = {'John': 425, 'Liz': 212, 'Isaac': 345}
            for new_token in new_tokens:
                if new_token in lista_invertida:
                    # lista_invertida[new_token] += 1
                    lista_invertida[new_token].append(auxDocNumber)
                else:
                    lista_invertida[new_token] = [auxDocNumber]

# tokens = set(tokens)

# print('\nStop words: ')
# print(stop_words)
# tokens = [w for w in tokens if not w.lower() in stop_words]
# tokens = sorted(tokens)

# lista_invertida = {}
# lista_invertida = []*10000
# lista_invertida = dict.fromkeys(tokens)

# p(lista_invertida)

with open(config['gli']['ESCREVA'], 'w') as fp:
    for p in lista_invertida.items():
        fp.write("%s;%s\n" % p)

        """ 
print('\nLista Invertida: ')
with open(config['gli']['ESCREVA'], mode='w') as gli_file:
    gli_writer = csv.writer(
        gli_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator='\n')
    gli_writer.writerow(
        ['Term', 'DocNumber'])
    for token in tokens[:loop_limiter]:
        auxDocNumbers = []
        for docXML in docsXML:
            doc = minidom.parse(docXML)
            records = doc.getElementsByTagName('RECORD')
            for record in records[:loop_limiter]:
                if record.getElementsByTagName('ABSTRACT'):
                    auxAbstract = record.getElementsByTagName('ABSTRACT')[
                        0].firstChild.data
                elif record.getElementsByTagName('EXTRACT'):
                    auxAbstract = record.getElementsByTagName('EXTRACT')[
                        0].firstChild.data
                else:
                    auxAbstract = 'XXXXXXXXXXXXXXXX '+record.getElementsByTagName('TITLE')[
                        0].firstChild.data

                for x in range(auxAbstract.upper().count(token)):
                    if record.getElementsByTagName(
                            'RECORDNUM'):
                        auxDocNumbers.append(int(record.getElementsByTagName(
                            'RECORDNUM')[0].firstChild.data))

        print("%30s  " % token, end='')
        print(auxDocNumbers)

        gli_writer.writerow(
            [token, auxDocNumbers])
 """

""" 

for docXML in docsXML:
    doc = minidom.parse(docXML)
    records = doc.getElementsByTagName('RECORD')
    for record in records[:loop_limiter]:
        if record.getElementsByTagName('ABSTRACT'):
            auxAbstract = record.getElementsByTagName('ABSTRACT')[
                0].firstChild.data
        elif record.getElementsByTagName('EXTRACT'):
            auxAbstract = record.getElementsByTagName('EXTRACT')[
                0].firstChild.data
        else:
            auxAbstract = record.getElementsByTagName('TITLE')[
                0].firstChild.data
        tokenizer = RegexpTokenizer(r'\w+')
        # new_tokens = tokenizer.tokenize(shave(auxAbstract))
        new_tokens = tokenizer.tokenize(auxAbstract.upper())
        # remove words smaller then 3 chars
        new_tokens = [f for f in new_tokens if len(f) > 2]
        # remove words with numbers
        new_tokens = [x for x in new_tokens if not any(c.isdigit() for c in x)]

        for new_token in new_tokens:
            if lista_invertida.__contains__(new_token):
                lista_invertida[new_token] += 1
            else:
                lista_invertida.append([new_token])
        p(lista_invertida) """

# # lista_invertida.extend(new_tokens)

# for i in range(2, _len_of_bag_of_words + 2):

#     # accesses the word from bag at i-th row and 1st col
#     word = _doc_sheet.cell(i, 1).value

#     # when a query has that word from bag
#     if _lemma_set.__contains__(word):
#         # then term-freq is accessed from query-lemma-set
#         tf = _lemma_set.get(word)
#         # tf is assigned to i-th row at query-col (58)
#         _doc_sheet.cell(i, 58).value = tf
#         # accesses the idf from i-th row at idf-col (60)
#         idf = float(_doc_sheet.cell(i, 60).value)
#         # multiplies tf and idf
#         value = float(format(tf * idf, ".5f"))
#         # assigns the product to query-column at i-th row
#         _doc_sheet.cell(i, 58).value = value
#     else:
#         # when a query does not have that word from bag
#         # tf is assigned 0 to i-th row at query-column
#         # multiplying idf would also give 0 because tf is zero
#         _doc_sheet.cell(i, 58).value = 0

# print(datetime.now().strftime("%H:%M:%S") + ": completed query tf-idf calculations...")


# tokens = [f for f in tokens if len(f) > 2]  # remove words smaller then 3 chars
# # remove words with numbers
# tokens = [x for x in tokens if not any(c.isdigit() for c in x)]
# tokens = set(tokens)


# stop_words = set(stopwords.words('english'))
# print('\nStop words: ')
# print(stop_words)
# tokens = [w for w in tokens if not w.lower() in stop_words]
# tokens = sorted(tokens)
# # print(tokens)


# print('\nLista Invertida: ')
# with open(config['gli']['ESCREVA'], mode='w') as gli_file:
#     gli_writer = csv.writer(
#         gli_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator='\n')
#     gli_writer.writerow(
#         ['Term', 'DocNumber'])

#     for token in tokens[:loop_limiter]:
#         auxDocNumbers = []
#         for docXML in docsXML:
#             doc = minidom.parse(docXML)
#             records = doc.getElementsByTagName('RECORD')
#             for record in records[:loop_limiter]:
#                 if record.getElementsByTagName('ABSTRACT'):
#                     auxAbstract = record.getElementsByTagName('ABSTRACT')[
#                         0].firstChild.data
#                 elif record.getElementsByTagName('EXTRACT'):
#                     auxAbstract = record.getElementsByTagName('EXTRACT')[
#                         0].firstChild.data
#                 else:
#                     auxAbstract = 'XXXXXXXXXXXXXXXX '+record.getElementsByTagName('TITLE')[
#                         0].firstChild.data

#                 for x in range(auxAbstract.upper().count(token)):
#                     if record.getElementsByTagName(
#                             'RECORDNUM'):
#                         auxDocNumbers.append(int(record.getElementsByTagName(
#                             'RECORDNUM')[0].firstChild.data))

#         print("%30s  " % token, end='')
#         print(auxDocNumbers)

#         gli_writer.writerow(
#             [token, auxDocNumbers])


# print('\nESPERADOS: '+config['pc']['ESPERADOS'])

# doc = minidom.parse(config['pc']['LEIA'])
# queries = doc.getElementsByTagName("QUERY")
# with open(config['pc']['ESPERADOS'], mode='w') as esperados_file:
#     esperados_writer = csv.writer(
#         esperados_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator='\n')
#     esperados_writer.writerow(
#         ['QueryNumber', 'DocNumber', 'DocVotes'])
#     for query in queries:
#         # aux = unidecode.unidecode(aux)
#         auxQueryNumber = query.getElementsByTagName('QueryNumber')[
#             0].firstChild.data
#         items = query.getElementsByTagName('Item')
#         for item in items:
#             auxDocNumber = item.firstChild.data
#             auxScore = item.getAttribute('score')
#             auxVotes = int(auxScore[0]) + int(auxScore[1]) + \
#                 int(auxScore[2]) + int(auxScore[3])
#             # print(votes)
#             esperados_writer.writerow(
#                 [auxQueryNumber, auxDocNumber, auxVotes])
#             # print(auxDocNumber)
