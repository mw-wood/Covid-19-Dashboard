def parse_csv_data(csv_filename = 'nation_2021-10-28.csv'):
    l = []
    with open(csv_filename, 'r') as f: #only retrieve first 7 lines
        for row in f:
            l.append(row.strip())
    return l

def process_covid_csv_data(covid_csv_data):    
    data = []
    
    seven_day_total = 0
    current_hospital_cases = 0
    total_deaths = 0

    for item in covid_csv_data:
        row = item.split(',') 
        row = row[4:] #total deaths, hospital cases, new cases
        data.append(row)

    data.remove(data[0]) #remove collumn headers
    
    for item in data:
        if item[0] != '':
            total_deaths = int(item[0])
            break
    
    current_hospital_cases = int(data[0][1])
    
    for i in range(2,9): #replace hardcoded values with config file - 2/9 doesnt work with all formats
        seven_day_total += int(data[i][2])

    return seven_day_total, current_hospital_cases, total_deaths     
        
print (process_covid_csv_data(parse_csv_data()))