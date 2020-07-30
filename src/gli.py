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


def shave(myString):

    # tokenizer = RegexpTokenizer(r'\w+')
    # myString = tokenizer.tokenize(myString)

    myString = myString.replace('"', '').replace(';', '').replace(
        '\n', ' ').replace('\r', '').replace('  ', ' ').replace('  ', ' ').upper()
    # myString = myString.str.findall('\w{4,}').str.join(' ')
    myString = unidecode.unidecode(myString)
    # myString = myString.replace(r'\b(\w{1,3})\b', '')
    return myString


config = ConfigParser()
config.read('./src/gli.cfg')
print('\n***Gerador de Lista Invertida***')

itemsLEIA = config['gli']['LEIA'].split(',')
for itemLEIA in itemsLEIA:
    # do something with path
    print('LEIA: '+itemLEIA)

tokens = []

for itemLEIA in itemsLEIA:
    doc = minidom.parse(itemLEIA)
    records = doc.getElementsByTagName('RECORD')
    for record in records[:10]:
        if record.getElementsByTagName('ABSTRACT'):
            auxAbstract = record.getElementsByTagName('ABSTRACT')[
                0].firstChild.data
        elif record.getElementsByTagName('EXTRACT'):
            auxAbstract = record.getElementsByTagName('EXTRACT')[
                0].firstChild.data
        else:
            auxAbstract = 'XXXXXXXXXXXXXXXX '+record.getElementsByTagName('TITLE')[
                0].firstChild.data
        tokenizer = RegexpTokenizer(r'\w+')
        # tokens += nltk.word_tokenize(shave(auxAbstract))
        tokens += tokenizer.tokenize(shave(auxAbstract))

tokens = [f for f in tokens if len(f) > 2]  # remove words smaller then 3 chars
# remove words with numbers
tokens = [x for x in tokens if not any(c.isdigit() for c in x)]
tokens = set(tokens)
tokens = sorted(tokens)
# print(tokens)

with open(config['gli']['ESCREVA'], mode='w') as gli_file:
    gli_writer = csv.writer(
        gli_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator='\n')
    gli_writer.writerow(
        ['Term', 'DocNumber'])

    for token in tokens[:5]:
        auxDocNumbers = []
        for itemLEIA in itemsLEIA:
            doc = minidom.parse(itemLEIA)
            records = doc.getElementsByTagName('RECORD')
            for record in records[:10]:
                if record.getElementsByTagName('ABSTRACT'):
                    auxAbstract = record.getElementsByTagName('ABSTRACT')[
                        0].firstChild.data
                elif record.getElementsByTagName('EXTRACT'):
                    auxAbstract = record.getElementsByTagName('EXTRACT')[
                        0].firstChild.data
                else:
                    auxAbstract = 'XXXXXXXXXXXXXXXX '+record.getElementsByTagName('TITLE')[
                        0].firstChild.data
                if token in auxAbstract.upper():
                    if record.getElementsByTagName(
                            'RECORDNUM'):
                        auxDocNumbers.append(int(record.getElementsByTagName(
                            'RECORDNUM')[0].firstChild.data))
                    # print(auxDocNumbers)

        print(token+'    '+str(auxDocNumbers))

        # aux = record.getElementsByTagName('QueryText')[0].firstChild.data
        # aux = unidecode.unidecode(aux)
        gli_writer.writerow(
            [token, auxDocNumbers])


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
