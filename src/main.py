

from configparser import ConfigParser
config = ConfigParser()
config.read('./cfg/general.cfg')
STEMMER = bool(config['general']['STEMMER'])
# if STEMMER:
#     print('1')
# else:
#     print('0')

import pc
import gli
import index
import busca
