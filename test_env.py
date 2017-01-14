import logging
import ConfigParser
import argparse
from wu_api import *


logformat = '%(asctime)s : %(levelname)s : %(message)s'
logging.basicConfig(format=logformat, filename='./out.log',level=logging.DEBUG)
config_path = '/home/jat/PycharmProjects/wu_api/test_config.cfg'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default=config_path, help='Config file, default {0}'.format(config_path))
    args = parser.parse_args()
    config_file = args.c
    conf_parser = ConfigParser.ConfigParser()
    conf_parser.read(config_file)

    api_secret = conf_parser.get('wu_api', 'api_secret')
    default_loc = conf_parser.get('wu_api', 'default_loc')

