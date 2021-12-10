'''This Module is responsible for storing and filtering news articles pulled
   from the NEWS API. The user should be responsible for providing an API key
   which can be obtained by signing up to their website (more in README.txt).
   These articles are then used by main.py to show within the flask application
   where they can be further customised.

   Variables:
       This module makes use of many global variables used across the various
       methods.

       Logging variables:
           These are responsable for logging events within this module at
           differing severity levels.
       Configeration Variables:
           Variables defined by the user within the configeration json file

    Procedures:
        news_API_request:
            This returns a selection of the top articles related to the parameters
            provided by the user in the config file. By default, this is set
            to "Covid COVID-19 coronavirus".
        update_news:
            filters and stores news articles depending on a blacklist provided
            by the flask application. It also limits the amount of articles
            stored in main.py to 5.
   '''

import json
import logging
from newsapi import NewsApiClient

config_file = 'config.json'  # configeration file

# Logging Variables
formatter = '%(asctime)s :: %(levelname)s :: %(message)s'
logging.basicConfig(filename='log.log',
                    format=formatter,)

log_debug = logging.getLogger('news_debug')
log_debug.setLevel(logging.DEBUG)

log_info = logging.getLogger('news_info')
log_info.setLevel(logging.INFO)

log_error = logging.getLogger('news_info')
log_error.setLevel(logging.ERROR)


def parse_json(config='config.json'):
    '''Parse Configeration File

    Keyword Argument:
    config -> config file to retrieve user settings (json)

    '''
    with open(config, 'r') as f:
        data = json.load(f)
    return data


# Configeration Variables
user_info = parse_json()[0]['User Information']
user_terms = user_info[0]['Covid Terms']
user_api_key = user_info[0]['API Key']


def news_API_request(covid_terms='Covid COVID-19 coronavirus'):
    '''Returns a dictionary of news articles from an API request

    Keyword Argument:
    covid_terms -> terms for the news api to retrieve articles containing (str)

    '''
    data = []

    newsapi = NewsApiClient(api_key=user_api_key)

    for term in covid_terms.split():
        top_headlines = newsapi.get_top_headlines(q=term)
        for article in top_headlines['articles']:
            data.append(article)
    log_debug.debug('Returned Articlces')
    return data


def update_news(blacklist=[]):
    '''Stores news articles and returns a curated selection

    Keyword Argument:
    blacklist -> list containing news article titles to be
                 excluded from updates (list)

    '''
    articles = []
    filtered_articles = []

    for item in news_API_request(user_terms):
        articles.append(item)

    for item in articles:
        if item['title'] not in blacklist and len(filtered_articles) < 5:
            log_debug.debug('Retrieved filtered article')
            item['content'] = str(item['content'])[:100] + '... URL = ' + item['url']
            filtered_articles.append(item)

    log_info.info('Returned filtered articles')
    return filtered_articles
