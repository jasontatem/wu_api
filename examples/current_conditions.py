import ConfigParser
import argparse
from wu_api import WUApi


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

    # Get current conditions and print a basic report

    cond = wu.conditions()
    city_name = cond['current_observation']['display_location']['city']
    temp_f = cond['current_observation']['temp_f']
    cond_desc = cond['current_observation']['weather']
    print('In {0} the temperature is {1}F and the current condition is {2}'.format(city_name, temp_f, cond_desc))


