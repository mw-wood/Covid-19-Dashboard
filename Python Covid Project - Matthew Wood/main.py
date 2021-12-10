'''This Module is responsible for launching the FLASK based application
   used to display the covid dashboard within a web browser. It makes use
   of other modules responsable for data handling.

   Variables:
       This module makes use of many global variables used across the various
       methods.

       Logging variables:
           These are responsable for logging events within this module at
           differing severity levels.
       Configeration Variables:
           Variables defined by the user within the configeration json file
       Module Variables:
           Global variables responsible for storing data vital to the operation
           of the flask application such as scheduled updates and news articles.

    Procedures:
        The procedures in this module are mainly responsible for recieving data
        from the URL of the flask website. They are also responsible for
        presenting news articles, converting timestamps to seconds and removing
        both news articles and scheduled updates.
   '''

import time
from datetime import datetime
import json
import logging
import sched
from flask import Flask, request, render_template
from covid_news_handling import update_news

import covid_data_handler as handler


def parse_json(config='config.json'):
    '''Parse Configeration File

    Keyword Argument:
    config -> config file to retrieve user settings (json)

    Returns:
    This function returns a dictionary from a json config
    '''
    with open(config, 'r') as f:
        data = json.load(f)
    return data


# Logging Variables
log_debug = logging.getLogger('data_debug')
log_debug.setLevel(logging.DEBUG)

log_info = logging.getLogger('data_info')
log_info.setLevel(logging.INFO)

log_warning = logging.getLogger('data_warning')
log_warning.setLevel(logging.WARNING)

log_error = logging.getLogger('data_error')
log_error.setLevel(logging.ERROR)

# Configeration File Variables
user_info = parse_json()[0]['User Information']

user_template_folder = user_info[0]['Website Templates Folder']
user_template = user_info[0]['Website Template']
user_app_title = user_info[0]['App Title']
user_app_route = user_info[0]['App Route']

user_url_info = parse_json()[2]['URL Information']

arg_article = user_url_info[0]['News Articles']
arg_name = user_url_info[0]['Update Name']
arg_time = user_url_info[0]['Update Time']
arg_covid_data = user_url_info[0]['Update Covid Data']
arg_news = user_url_info[0]['Update News']
arg_repeat = user_url_info[0]['Repeat Update']
arg_removed_update = user_url_info[0]['Removed Update']


# Module variables
app = Flask(__name__, template_folder=user_template_folder)

s = sched.scheduler(time.time, time.sleep)

news_blacklist = []
updates_list = []
news = []


@app.route(user_app_route, methods=['GET'])
def start_app():
    log_debug.debug('App Started Succesfully')
    handler.schedule_covid_updates(get_schedule_data()[0], get_schedule_data()[1])
    remove_update()
    remove_news()

    s.run(blocking=False)

    return render_template(user_template,
                           title=user_app_title,
                           news_articles=news,
                           updates=updates_list,
                           deaths_total=handler.deaths,
                           local_7day_infections=handler.local_7day,
                           location=handler.get_locations()[0],
                           national_7day_infections=handler.national_7day,
                           nation_location=handler.get_locations()[2],
                           hospital_cases=handler.hospital_cases_temp
                           )


def add_news():
    '''Updates the news articles used within the flask template'''
    global news
    news = update_news(news_blacklist)
    log_debug.debug('Updated News Articles')


def remove_news():
    '''Removes selected article from news dictionary'''
    if request.method == 'GET':
        removed_title = request.args.get(arg_article)
        log_debug.debug('Retrieved Article Title')
        if request.args.get(arg_article) is not None:
            news_blacklist.append(removed_title)
            log_debug.debug('Blacklist Updated')
            add_news()


def get_schedule_data():
    '''Retrieves update information

    Returns:
    Returns all URL variables that are valid
    '''
    if request.method == 'GET':
        request_name = request.args.get(arg_name)
        request_content = request.args.get(arg_time)
        request_news = request.args.get(arg_news)
        request_covid = request.args.get(arg_covid_data)
        request_repeat = request.args.get(arg_repeat)
    log_debug.debug('Retrieved URL Information')
    return request_name, request_content, request_news, request_covid, request_repeat


def remove_update():
    '''Allows the user to manually remove updates'''
    if request.args.get('update_item') is not None:  # remove update
        for item in updates_list:
            if request.args.get('update_item') == item['title']:
                if (item['covid_data'] is not False
                        and item['covid_data'] in s.queue):
                    s.cancel(item['covid_data'])
                if item['news'] is not False and item['news'] in s.queue:
                    s.cancel(item['news'])
                if item['auto_remove'] in s.queue:
                    s.cancel(item['auto_remove'])
                log_debug.debug('Succesfully Cancelled Update')
                updates_list.remove(item)
    log_error.error('Invalid remove request')


def get_time(url_time):
    '''Returns the time until the next scheduled update in seconds

    Keyword Argument:
    url_time -> the timestamp retrieved from the URL
                indicating when the update should execute
                (String)
    '''
    current_time = datetime.today().replace(microsecond=0)

    if url_time is not None:
        event_time = url_time + ':00'

        newtime = datetime.strptime(event_time, '%H:%M:%S')
        newtime = newtime.replace(year=current_time.year,
                                  month=current_time.month,
                                  day=current_time.day,
                                  microsecond=0)

        if newtime < current_time:
            day_temp = newtime.day + 1
            newtime = newtime.replace(day=day_temp, microsecond=0)

        time_difference = (newtime - current_time)

        log_debug.debug('Returned update time in seconds')
        return time_difference.total_seconds()
    log_warning.warning('User did not enter time')
    return None


if __name__ == '__main__':
    updates_list = handler.scheduled_updates
    add_news()
    handler.update_covid_data()
    app.run()
