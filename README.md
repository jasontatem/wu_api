# wu_api: A simple Weather Underground API client

## Overview

This is intended to be a convenience layer and assumes some familiarity with the API exposed by weatherunderground.com.  Limited functionality will be expaneded over time.

More information about the underlying API, as well as information about obtaining an API key, can be found [here](https://www.wunderground.com/weather/api/). This [page](https://www.wunderground.com/weather/api/d/docs?d=data/index&MR=1) is very useful as it contains examples of the expected data formats for various options.

## General Usage

### To create an API client session:
```python
>>> from wu_api import WUApi
>>> wu = WUApi(<api_secret>, <default_location>)
```

API secret is required and can be obtained from Weather Underground.  Low volume usage is free, higher volumes may require paying for a higher tier of service.

Default location can be specified in a variety of formats.  See example default_loc values in config_sample.cfg. 

### To query data:

Get current conditions at your default location: 
```python
>>> data = wu.get_conditions()
>>> data['current_observation']['temp_f']
32.5
```

Get current conditions for a different location:
```python
>>> data = wu.get_conditions(location='Ireland/Dublin')
>>> data['current_observation']['temp_f']
45
>>> data['current_observation']['temp_c']
7
```

Get historical data for June 1, 2016 for Singapore, note different names for temperature keys (tempi / tempm versus temp_f / temp_c):
```python
>>> data = wu.get_history(location='Singapore/Singapore', hist_date='20160601')
>>> data['history']['observations'][0]['date']
{u'mday': u'01', u'hour': u'00', u'min': u'00', u'mon': u'06', u'pretty': u'12:00 AM SGT on June 01, 2016', u'year': u'2016', u'tzname': u'Asia/Singapore'}
>>> data['history']['observations'][0]['tempi']
u'82.4'
>>> data['history']['observations'][0]['tempm']
u'28.0'
```

Accumulate a range of days of historical data, returns a list of objects identical to those in the previous example:
```python
>>> data = wu.get_history_daterange(start_date='20160601', end_date='20160608')
```

## Example Code

test_env.py contains example code for creating an API session.  Copy config_sample.cfg to test_config.cfg and edit th
e api_secret and default_loc values as appropriate.

## Security Warning

For whatever reason, Weather Underground's API requires the API key to be included in the URL of every request.  If logging is enabled (as it is in test_env.py), the API key may be written to log files every time an API call occurs.

Though the use of HTTPS (which this class does, don't modify base_url without a good reason to) mitigates some of the issues with putting the one and only security key into the URL, there are substantial additional risks of data leakage including the API key.  It is best to consider a WU API token at high risk of compromise and monitor its usage closely.  Avoid accessing WU API URLs via browsers to prevent having the API key available in browser URL history. 
