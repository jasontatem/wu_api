import logging
import ConfigParser
import argparse
from wu_api import WUApi


# Logging configuration.  Comment out to disable, enable

log_format = '%(asctime)s : %(levelname)s : %(message)s'
logging.basicConfig(format=log_format, filename='./out.log',level=logging.DEBUG)

if __name__ == '__main__':

    # Get config path from command line args

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default='./test_config.cfg', help='Config file path, default ./test_config.cfg')
    args = parser.parse_args()

    # Load config file

    conf_parser = ConfigParser.ConfigParser()
    conf_parser.read(args.c)

    api_secret = conf_parser.get('wu_api', 'api_secret')
    default_loc = conf_parser.get('wu_api', 'default_loc')

    # Create WUApi object

    wu = WUApi(api_secret, default_loc=default_loc)


