'''Json Config Initialisation'''

import json

result = []

user_info = {'User Information': [{'API Key': '(Your Api Key)',
                                   'Covid Terms': 'Covid COVID-19 coronavirus',
                                   'Covid dataset (csv)': 'nation_2021-10-28.csv',
                                   'Website Templates Folder': 'templates',
                                   'Website Template': 'index.html',
                                   'App Title': 'Daily Update',
                                   'App Route': '/index',
                                   }]}

user_locations = {'Location Information': [{'Nation': 'England',
                                            'Nation Type': 'nation',
                                            'Local Area': 'Exeter',
                                            'Local Type': 'ltla'
                                            }]}

url_parameters = {'URL Information': [{'News Articles': 'notif',
                                       'Update Name': 'two',
                                       'Update Time': 'update',
                                       'Update Covid Data': 'covid-data',
                                       'Update News': 'news',
                                       'Repeat Update': 'repeat',
                                       'Removed Update': 'update_item',
                                       }]}

result.extend((user_info, user_locations, url_parameters))

json_config = json.dumps(result, indent=4)

with open('config.json', 'w') as jsonfile:
    jsonfile.write(json_config)
