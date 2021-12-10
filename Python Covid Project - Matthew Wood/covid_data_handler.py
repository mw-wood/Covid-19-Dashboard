'''This Module is responsible for parsing and processing coronavirus data
   and both scheduling and storing future updates to news and covid data to be used
   within the main.py module.

   Variables:
       This module makes use of many global variables used across the various
       methods.

       Logging variables:
           These are responsable for logging events within this module at
           differing severity levels.
       Configeration Variables:
           Variables defined by the user within the configeration json file
       Module Variables:
           Global variables responsible for storing the values of necessary
           covid data to be used in main.py as well as scheduled future updates.
           The global constand SECONDS_IN_DAY is also defined here.

    Procedures:
        The most important procedures within this module include are responsible
        for scheduling flask updates, parsing and processing covid API data,
        automatically removing updates once executed, and processing data
        from a given csv file.

        There exists other methods that are responsible for confirming the
        validity of their selected parameters within a dataset.
   '''

import json
import logging
import sched
import time
from uk_covid19 import Cov19API
import main


def parse_json(config='config.json'):
    '''Parse Configeration File

    Keyword Argument:
    config -> config file to retrieve user settings (json)

    '''
    with open(config, 'r') as f:
        data = json.load(f)
    return data


# loggers
log_debug = logging.getLogger('data_debug')
log_debug.setLevel(logging.DEBUG)

log_info = logging.getLogger('data_info')
log_info.setLevel(logging.INFO)

log_warning = logging.getLogger('data_warning')
log_warning.setLevel(logging.WARNING)

log_error = logging.getLogger('data_error')
log_error.setLevel(logging.ERROR)

# Config Variables
user_info = parse_json()[0]['User Information']
user_dataset = user_info[0]['Covid dataset (csv)']

user_locations = parse_json()[1]['Location Information']
user_nation = user_locations[0]['Nation']
user_nation_type = user_locations[0]['Nation Type']
user_local = user_locations[0]['Local Area']
user_local_type = user_locations[0]['Local Type']

# Module Variables
scheduled_updates = []

national_7day = 0
local_7day = 0

deaths = ''
hospital_cases_temp = ''

SECONDS_IN_DAY = 86400

s = sched.scheduler(time.time, time.sleep)


def schedule_covid_updates(update_name, update_interval):
    '''Schedules both news and covid updates

    Keyword Arguments:
    update Name -> The name chosen by the user for the scheduled update (str)
    update_interval -> the timestamp retrieved from the URL
                       indicating when the update should execute
                       (String)
    '''
    update = {}

    request_news = main.get_schedule_data()[2]
    request_covid = main.get_schedule_data()[3]
    request_repeat = main.get_schedule_data()[4]

    if (None not in (update_name, update_interval)
            and '' not in (update_name, update_interval)):
        update_seconds = main.get_time(update_interval)
        if check_unique_name(update_name):
            log_debug.debug('Valid Update Name Entered')
            update['title'] = update_name  # make unique names

            if request_news == main.arg_news:
                update['news'] = s.enter(update_seconds,
                                         1,
                                         main.add_news,
                                         )
            else:
                update['news'] = False

            if request_covid == main.arg_covid_data:
                update['covid_data'] = s.enter(update_seconds,
                                               1,
                                               update_covid_data)
            else:
                update['covid_data'] = False

            if request_repeat == main.arg_repeat:
                update['repeat'] = True
            else:
                update['repeat'] = False

            update['auto_remove'] = s.enter(update_seconds,
                                            2,
                                            auto_remove_update,
                                            (update,))

            if update['covid_data'] is not False:
                covid_temp = True
            else:
                covid_temp = False
            if update['news'] is not False:
                news_temp = True
            else:
                news_temp = False

            update['content'] = ('Updating Covid Data: '
                                 + str(covid_temp),
                                 'Updating News: ', str(news_temp),
                                 'Repeating?: ', update['repeat'],
                                 'at ', str(update_interval))

            scheduled_updates.append(update)
            log_info.info('Update Succesfully Scheduled')

        else:
            log_info.info('Update Name Already Exists')
    else:
        log_warning.warning('Invalid Update Name or Time')

    s.run(blocking=False)


def auto_remove_update(update):
    '''Schedules to automatically remove an update

    Keyword argument:
    Update: the specified update to be removed (dictionary)

    '''
    for item in scheduled_updates:
        if item['title'] == update['title']:  # finds if update is scheduled
            if item['repeat']:  # if repeat is true, re-schedule the update
                item['title'] = item['title'] + ' (Repeat)'  # changes the title of the update

                item['repeat'] = False  # turns off auto-repeat

                if item['covid_data'] is not False:  # re-schedules covid update
                    s.enter(SECONDS_IN_DAY,          # to execute in 24 hours
                            1,
                            update_covid_data)

                if item['news'] is not False:  # re-schedules news update
                    s.enter(SECONDS_IN_DAY,    # to execute in 24 hours
                            1,
                            main.add_news)

                item['auto_remove'] = s.enter(SECONDS_IN_DAY,  # always removed
                                              2,
                                              auto_remove_update,
                                              (update,))
                s.run(blocking=False)
                log_info.info('Re-scheduled Update')
            else:
                log_info.info('Automatically Removed Update')
                scheduled_updates.remove(item)  # if repeat is false, remove update


def update_covid_data():
    '''Recieves current data from an API request & updates global variables'''
    global national_7day
    global local_7day
    global deaths
    global hospital_cases_temp

    nat_data = process_api_data(covid_API_request
                                (get_locations()[2],
                                 get_locations()[3]))
    loc_data = process_api_data(covid_API_request
                                (get_locations()[0],
                                 get_locations()[1]))

    national_7day = nat_data[0]
    local_7day = loc_data[0]

    deaths = 'Total Deaths: ' + str(nat_data[2])
    hospital_cases_temp = 'Hospital Cases: ' + str(nat_data[1])
    log_debug.debug('Updated Covid Variables')


def check_unique_name(update_name):
    ''' Checks string input against all update titles in scheduled updates

    Keyword argument:
    update_name -> name user is trying to assign to a scheduled update (str)

    '''
    log_debug.debug('Checking Entered Name')
    for item in scheduled_updates:
        if update_name in item['title']:  # if update_name exists in updates,
            print(item['title'])          # return false
            return False
    return True


def parse_csv_data(csv_filename='nation_2021-10-28.csv'):
    '''Returns dataset from a provided CSV

    Keyword argument:
    csv_filename -> name of the dataset (str)

    '''
    output_list = []
    try:
        with open(csv_filename, 'r') as f:
            for row in f:
                output_list.append(row.strip())
        return output_list
    except:
        log_error.error('Failed to read csv, please check filename or directory')


def process_covid_csv_data(covid_csv_data=parse_csv_data()):
    '''Returns required variables from provided dataset

    Keyword argument:
    covid_csv_data -> dataset in which data will be processed from (function)

    '''
    data = []

    seven_day_total = 0
    current_hospital_cases = 0
    total_deaths = 0

    for item in covid_csv_data:
        row = item.split(',')
        row = row[4:]  # total deaths, hospital cases, new cases
        data.append(row)

    data.remove(data[0])  # remove collumn headers

    for item in data:
        if isinstance(item[0], int) or item[0] != '':
            total_deaths = int(item[0])
            break

    current_hospital_cases = int(data[0][1])

    for i in range(2, 9):
        seven_day_total += int(data[i][2])

    log_debug.debug('Returned csv data')
    return seven_day_total, current_hospital_cases, total_deaths


def covid_API_request(location='Exeter',
                      location_type='ltla'):
    '''Returns either local or national data depending on the arguments

    Keyword Arguments:
    location -> region in which the covid data will be retrieved from (str)
    location_type -> location type for the specified location (str)

    '''
    api_filters = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    if location_type == user_nation_type:
        new_cases = "newCasesByPublishDate"
    else:
        new_cases = "newCasesBySpecimenDate"

    cases_and_deaths = {
            "cumulativeDeaths": "cumDeaths28DaysByPublishDate",
            "hospital_cases": "hospitalCases",
            "newCases": new_cases,
    }

    try:
        api = Cov19API(filters=api_filters,
                       structure=cases_and_deaths,
                       )

        data = api.get_json()
        return data
    except:
        log_error.error('Failed to retrieve API data')


def process_api_data(dictionary=covid_API_request()):
    '''Returns required values from an API call

    Keyword Argument:
    dictionary -> data from the coronavirus api (dict)

    '''
    data = dictionary['data']

    hospital_cases = check_in_data('hospital_cases', data)
    total_deaths = check_in_data('cumulativeDeaths', data)
    seven_day_total = 0

    for x in range(1, 8):
        seven_day_total += data[x]['newCases']  # data from the last 7 days

    log_debug.debug('Returned API Data')
    return seven_day_total, hospital_cases, total_deaths


def check_in_data(field, data):
    '''Checks if the values within the data are valid

    Keyword arguments:
    field -> data field to be compared against (str)
    data -> dataset to check within (list)

    '''
    for x in range(len(data)-1):
        if isinstance(data[x][field], int) or data[x][field] is not None:
            output = data[x][field]
            log_debug.debug('Valid in data')
            return output
    log_warning.warning('No valid values in file')
    return None


def get_locations():
    '''Returns both local and national locations'''
    log_debug.debug('Returned Location Data')
    return user_local, user_local_type, user_nation, user_nation_type
