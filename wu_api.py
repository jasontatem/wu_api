import requests
import time
import datetime
import logging


def epoch_to_yyyymmdd(epoch_time):
    return time.strftime('%Y%m%d', time.gmtime(epoch_time))


def today_yyyymmdd():
    return epoch_to_yyyymmdd(time.time())


class WUApi(object):
    def __init__(self, api_key, base_url='https://api.wunderground.com/api/'):
        self.api_key = api_key
        self.base_url = base_url + self.api_key

    def call_wu_api(self, features, location):
        if type(features) == str:
            features_url = '/{0}'.format(features)
        elif type(features) == list:
            features_url = '/' + '/'.join(features)
        else:
            raise ValueError('features param should be a string for single feature query or list of strings for multi feature query')
        location_url = '/q/{0}'.format(location)
        full_url = self.base_url + features_url + location_url + '.json'
        logging.debug('Calling WU API with URL: {0}'.format(full_url))
        return requests.get(full_url).json()

    def get_conditions(self, location):
        return self.call_wu_api('conditions', location)

    def get_history(self, location, hist_date=today_yyyymmdd()):
        return self.call_wu_api('history_{0}'.format(hist_date), location)

    def get_history_daterange(self, location, start_date, end_date):
        start_dt = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_dt = datetime.datetime.strptime(end_date, '%Y%m%d')
        query_dt = start_dt
        results = list()
        while query_dt <= end_dt:
            query_yyyymmdd = query_dt.strftime('%Y%m%d')
            results.append(self.get_history(location, query_yyyymmdd))
            query_dt = query_dt + datetime.timedelta(days=1)
        return results

