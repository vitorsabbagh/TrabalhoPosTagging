import unidecode
from configparser import ConfigParser
from xml.dom import minidom
import xml.etree.cElementTree as ET
import csv

# from ConfigParser import ConfigParser # for python3
data_file = './src/pc.cfg'

config = ConfigParser()

config.read(data_file)
print('\n***Processador de Consultas***')
print('LEIA: '+config['pc']['LEIA'])


doc = minidom.parse(config['pc']['LEIA'])
# print(doc)
queries = doc.getElementsByTagName("QUERY")

authors_new = ET.Element("authors")

# ET.SubElement(authors_new, "AUTHORS").text = query.firstChild.data


# tree = ET.ElementTree(authors_new)
# tree.write("authors.xml")

with open(config['pc']['CONSULTAS'], mode='w') as employee_file:
    employee_writer = csv.writer(
        employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator='\n')
    employee_writer.writerow(
        ['Query Number', 'Query Text'])
    for query in queries:
        aux = query.getElementsByTagName("QueryText")[0].firstChild.data
        aux = unidecode.unidecode(aux)
        employee_writer.writerow(
            [query.getElementsByTagName("QueryNumber")[0].firstChild.data, aux.upper().replace('"', '').replace(';', '').replace('\n', ' ').replace('\r', '').replace('  ', ' ').replace('  ', ' ')])
        # print(
        #     query.getElementsByTagName("QueryText")[0].firstChild.data)
        # print(
        #     query.getElementsByTagName("QueryNumber")[0].firstChild.data)

    # employee_writer.writerow([author.firstChild.data, 'IT'])
