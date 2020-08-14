
import PorterStemmer
import logging
# import pprint
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
# from nltk import FreqDist
# nltk.download('punkt')
nltk.download('stopwords')


logging.basicConfig(filename='buscador.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Iniciando Gerador de Lista Invertida')

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


logging.info('Iniciando leitura do arquivo de configuração')
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


ps = PorterStemmer.PorterStemmer()
config.read('./cfg/general.cfg')
STEMMER = eval(config['general']['STEMMER'])
# if STEMMER:
#     import PorterStemmer
#     ps = PorterStemmer()
#     for stop_word in stop_words
#         stop_word = ps.stem(stop_word, 0, len(stop_word)-1)
#         p(stop_word)


new_tokens = []
logging.info('Iniciando geração de lista invertida')
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

            # if STEMMER:
            #     for new_token in new_tokens:
            #         new_token = ps.stem(new_token.lower(), 0, len(new_token)-1)
            # p(new_token, end=' -> ')
            # p(ps.stem(new_token.lower(), 0, len(new_token)-1))

            # tokens += tokenizer.tokenize(shave(auxAbstract))
            # lista_invertida = {'John': 425, 'Liz': 212, 'Isaac': 345}
            for new_token in new_tokens:
                # if new_token in lista_invertida:
                if STEMMER:
                    new_token = ps.stem(new_token.lower(),
                                        0, len(new_token) - 1).upper()
                if new_token in lista_invertida:
                    lista_invertida[new_token].append(auxDocNumber)
                else:
                    lista_invertida[new_token] = [auxDocNumber]
# p(lista_invertida)
logging.info('Finalizado processamento de lista invertida')

with open(config['gli']['ESCREVA'], 'w') as fp:
    for p in lista_invertida.items():
        fp.write("%s;%s\n" % p)

logging.info('Finalizada gravação de lista invertida')
logging.info('\n\n')
