import requests
import datetime
import logging


def today_yyyymmdd():
    return datetime.date.today().strftime('%Y%m%d')


def yesterday_yymmdd():
    return (datetime.date.today() - datetime.timedelta(1)).strftime('%Y%m%d')


class WUApi(object):
    def __init__(self, api_key, default_loc='CA/San_Francisco', base_url='https://api.wunderground.com/api/'):
        self.api_key = api_key
        self.base_url = base_url + self.api_key
        self.default_loc = default_loc

    def call_wu_api(self, features, location=None):
        if location is None:
            location = self.default_loc
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

    def get_conditions(self, location=None):
        return self.call_wu_api('conditions', location)

    def get_history(self, location=None, hist_date=today_yyyymmdd()):
        return self.call_wu_api('history_{0}'.format(hist_date), location)

    def get_history_daterange(self, location=None, start_date=yesterday_yymmdd(), end_date=today_yyyymmdd()):
        start_dt = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_dt = datetime.datetime.strptime(end_date, '%Y%m%d')
        query_dt = start_dt
        results = list()
        while query_dt <= end_dt:
            query_yyyymmdd = query_dt.strftime('%Y%m%d')
            results.append(self.get_history(location, query_yyyymmdd))
            query_dt = query_dt + datetime.timedelta(days=1)
        return results

