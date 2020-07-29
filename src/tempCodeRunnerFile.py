from configparser import ConfigParser
# from ConfigParser import ConfigParser # for python3
data_file = 'pc.cfg'
print('asd')
config = ConfigParser()
config.read(data_file)

config.sections()
# ['managers', 'workers']