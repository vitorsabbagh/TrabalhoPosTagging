import unidecode
from configparser import ConfigParser
from xml.dom import minidom
import xml.etree.cElementTree as ET
import csv

import logging
logging.basicConfig(filename='buscador.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('Iniciando Processamento de Consultas')

config = ConfigParser()
logging.info('Iniciando leitura do arquivo de configuração')
config.read('./cfg/pc.cfg')
print('\n***Processador de Consultas***')
print('LEIA: '+config['pc']['LEIA'])

logging.info('Iniciando leitura do arquivo XML de consultas')
doc = minidom.parse(config['pc']['LEIA'])
queries = doc.getElementsByTagName("QUERY")
with open(config['pc']['CONSULTAS'], mode='w') as queries_file:
    writer = csv.writer(
        queries_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator='\n')
    # writer.writerow(
    #     ['Query Number', 'Query Text'])
    for query in queries:
        aux = query.getElementsByTagName('QueryText')[0].firstChild.data
        aux = unidecode.unidecode(aux)
        writer.writerow(
            [query.getElementsByTagName('QueryNumber')[0].firstChild.data, aux.upper().replace('"', '').replace(';', '').replace('\n', ' ').replace('\r', '').replace('  ', ' ').replace('  ', ' ')])

logging.info('Finalizada gravação das consultas em CSV')

logging.info(
    'Iniciando leitura do arquivo de pontuação dos pesquisadores (ESPERADOS)')
print('\nESPERADOS: '+config['pc']['ESPERADOS'])

doc = minidom.parse(config['pc']['LEIA'])
queries = doc.getElementsByTagName("QUERY")
with open(config['pc']['ESPERADOS'], mode='w') as esperados_file:
    esperados_writer = csv.writer(
        esperados_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator='\n')
    esperados_writer.writerow(
        ['QueryNumber', 'DocNumber', 'DocVotes'])
    for query in queries:
        # aux = unidecode.unidecode(aux)
        auxQueryNumber = query.getElementsByTagName('QueryNumber')[
            0].firstChild.data
        items = query.getElementsByTagName('Item')
        for item in items:
            auxDocNumber = item.firstChild.data
            auxScore = item.getAttribute('score')
            auxVotes = int(auxScore[0]) + int(auxScore[1]) + \
                int(auxScore[2]) + int(auxScore[3])
            # print(votes)
            esperados_writer.writerow(
                [auxQueryNumber, auxDocNumber, auxVotes])
            # print(auxDocNumber)

logging.info('Finalizada gravação dos resultados esperadas')
