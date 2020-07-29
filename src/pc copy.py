import configparser

config = configparser.ConfigParser()

print(config.sections())

config.read('./src/pc.cfg')

print(config.sections())
# config.sections()
