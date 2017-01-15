import requests
import datetime
import logging


def today_yyyymmdd():
    """
    Returns today's date in yyyymmdd format as used by many WU API endpoints
    :return:
    """
    return datetime.date.today().strftime('%Y%m%d')


def yesterday_yymmdd(delta=1):
    """
    Returns yesterday's (or further back) date in yyyymmdd format as used by many WU API endpoints
    :return:
    """
    return (datetime.date.today() - datetime.timedelta(delta)).strftime('%Y%m%d')


class WUApi(object):
    def __init__(self, api_key, default_loc='CA/San_Francisco', base_url='https://api.wunderground.com/api/', language='EN', bestforecast_enable=True):
        """
        Init function for WUApi class, creates an instance of WUApi
        :param api_key: Secret key issued by Weather Underground
        :param default_loc: Default location will be used on all queries if no other location is provided
        :param base_url: Base URL for building API calls
        :param language: Language code, see https://www.wunderground.com/weather/api/d/docs?d=language-support for supported languages
        :param bestforecast_enable: Set to False to disable WU's BestForecast feature (https://www.wunderground.com/about/data)
        """
        self.api_key = api_key
        self.language = language
        self.bestforecast_enable = bestforecast_enable
        self.api_base = base_url
        self.build_base_url()
        if not self.bestforecast_enable:
            bfc_url = '/bestfct:0'
        else:
            bfc_url = ''
        self.base_url = base_url + self.api_key + '/lang:{0}'.format(self.language) + bfc_url
        self.default_loc = default_loc

    def build_base_url(self):
        """
        Rebuilds the base URL including API key, language option, and BestForecast option
        Can be used to regenerate the base URL if any of these are changed after object
        instantiation.
        :return: Returns self.base_url contents and updates self.base_url
        """
        if not self.bestforecast_enable:
            bfc_url = '/bestfct:0'
        else:
            bfc_url = ''
        self.base_url = self.api_base + self.api_key + '/lang:{0}'.format(self.language) + bfc_url
        return self.base_url

    def call_wu_api(self, features, location=None):
        """
        Base function for WU API interaction

        WU API supports multiple data collections in a single request by
        chaining them in the URL, like '/hourly/conditions/...' to get both
        hourly forecast data and current conditions data in a single API call.
        This is supported by call_wu_api() by allowing either a str or list
        in the features param.  The URL will be built for a single or multiple
        collection request depending on the data type.

        :param features: String or list of strings representing feature(s) to collect
        :param location: Location identifier
        :return: Result of requests.get(<constructed API url>).json()
        """
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

    def conditions(self, location=None):
        """
        Current conditions for specified location
        :param location: Location identifier
        :return: Dict containing response from 'conditions' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/conditions
        """
        return self.call_wu_api('conditions', location)

    def history(self, location=None, hist_date=today_yyyymmdd()):
        """
        Historical conditions for specified location and date
        :param location: Location identifier
        :param hist_date: Historical date in yyyymmdd format, defaults to today's date (midnight to current result)
        :return: Dict containing response from 'history' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/history
        """
        return self.call_wu_api('history_{0}'.format(hist_date), location)

    def istory_daterange(self, location=None, start_date=yesterday_yymmdd(), end_date=today_yyyymmdd()):
        """
        Historical conditions for specified location and date range. Effectively an automated
        way to make multiple history() calls. Results are accumulated in a list, each
        list entry is the same as a history() result.
        :param location: Location identifier
        :param start_date: Start date in yyyymmdd format, defaults to yesterdays's date
        :param end_date: Historical date in yyyymmdd format, defaults to today's date
        :return: List of dicts containing response from 'history' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/history
        """
        start_dt = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_dt = datetime.datetime.strptime(end_date, '%Y%m%d')
        query_dt = start_dt
        results = list()
        while query_dt <= end_dt:
            query_yyyymmdd = query_dt.strftime('%Y%m%d')
            results.append(self.history(location, query_yyyymmdd))
            query_dt = query_dt + datetime.timedelta(days=1)
        return results

    def hourly_forecast_36h(self, location=None):
        """
        36h hourly forecast for specified location
        :param location: Location identifier
        :return: Dict containing response from 'hourly' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/hourly
        """
        return self.call_wu_api('hourly', location)

    def hourly_forecast_10d(self, location=None):
        """
        10d hourlu forecast for specified location
        :param location: Location identifier
        :return: Dict containing response from 'hourly10day' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/hourly10day
        """
        return self.call_wu_api('hourly10day', location)

    def forecast_3d(self, location=None):
        """
        3d daily forecast for specified location
        :param location: Location identifier
        :return: Dict containing response from 'forecast' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/forecast
        """
        return self.call_wu_api('forecast', location)

    def forecast_10d(self, location=None):
        """
        10d daily forecast for specified location
        :param location: Location identifier
        :return: Dict containing response from 'forecast10d' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/forecast10day
        """
        return self.call_wu_api('forecast10day', location)

    def geolookup(self, location=None):
        """
        Find geographical information such as city / state, postal code, lat / long, nearby PWS
        :param location: Location identifier
        :return: Dict containing response from 'geolookup' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/geolookup
        """
        return self.call_wu_api('geolookup', location)

    def alerts(self, location=None):
        """
        Weather alerts and special notices
        :param location: Location identifier
        :return: Dict containing response from 'alerts' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/alerts
        """
        return self.call_wu_api('alerts', location)

    def almanac(self, location=None):
        """
        Historical record high and low temperature information
        :param location: Location identifier
        :return: Dict containing response from 'almanac' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/almanac
        """
        return self.call_wu_api('almanac', location)

    def astronomy(self, location=None):
        """
        Astronomy information - moon cycle, sunrise / sunset times
        :param location: Location identifier
        :return: Dict containing response from 'astronomy' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/astronomy
        """
        return self.call_wu_api('astronomy', location)

    def planner(self, location=None, start_mmdd=today_yyyymmdd()[0:4], end_mmdd=yesterday_yymmdd(delta=-30)[0:4]):
        """
        "Travel planner" - shows historical averages for a given date range.  Start and
        end dates must not be more than 30 days apart.  A year cannot be specified.
        :param location: Location identifiter
        :param start_mmdd: Start date in 'mmdd' format
        :param end_mmdd: End date in 'mmdd' format
        :return: Dict containing response from 'planner' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/planner
        """
        return self.call_wu_api('planner_{0}{1}'.format(start_mmdd, end_mmdd), location)

    def tidal(self, location=None):
        """
        Tidal info such as maximum and minimum heights
        :param location: Location identifier
        :return: Dict containing response from 'tide' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/tide
        """
        return self.call_wu_api('tide', location)

    def raw_tidal(self, location=None):
        """
        "Raw" tidal info - streamlined for graphing purposes
        :param location: Location identifier
        :return: Dict containing response from 'rawtide' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/rawtide
        """
        return self.call_wu_api('rawtide', location)

    def webcams(self, location=None):
        """
        URLs and metadata for webcams near the specified location
        :param location: Location identifier
        :return: Dict containing response from 'webcams' endpoint, fields can be found at https://www.wunderground.com/weather/api/d/docs?d=data/webcams
        """
        return self.call_wu_api('webcams', location)


