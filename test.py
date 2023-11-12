from bs4 import BeautifulSoup
from lxml.cssselect import CSSSelector
import requests, os
import csv

## can use lxml for fast HTML parsing or default 'html.parser'
## URL Format: https://animecons.com/events/schedule.php?loc=usOH&year=2023

## Global Modules
bs = BeautifulSoup
rq = requests
css = CSSSelector

## ingridients
# https://animecons.com/events/schedule.php?loc=usOH&year=2023
base_url = 'https://animecons.com/events/schedule.php'
prio_locations = ['OH', 'IN', 'IL', 'KY']
meh_locations = ['TX', 'NYC']

print('What state?')
state = input()
print('What year?')
year = input()

url = base_url + '?loc=us' + state + '&year=' + year

## GET PAGE ##
src = rq.get(url).text
from_page = bs(src, 'lxml')

###################
## Ready to cook ##
###################

event_row = '#ConListTable tbody tr'
event_row_path = event_row + ' td a'
event_date = event_row + ' > td:nth-of-type(2)'
event_loc = event_row + ' > td:nth-of-type(3)'

events = from_page.select(event_row_path)
dates = from_page.select(event_date)
location = from_page.select(event_loc)

csvData = [
    # Headers
    {"column_01":"Event Name", "column_02":"Google Maps URL", "column_03": "Event Dates", "column_04":"Event Convention Name", "column_05":"Event City/State", "column_06":"Convention Website URL"}
]

print('appending ' +  str(len(events)) + ' events to csv file.')

with open('anime_con_scrap_' + state + '_' + year + '.csv', mode='w', newline='') as csvfile:
    for i in range(0, len(events)):
        print('creating spreadsheet row for [' + events[i].text + '].....')

        ev_name = events[i].text.strip(' 2023')
        ev_date = dates[i].text.replace(', 2023', '')
        ## some_html.get_text(separator=" ").strip() this will replace html tags with whatever
        ev_space = location[i].find('br').previous_sibling
        ev_cityState = location[i].find('br').next_sibling

        #Get google maps URL from convention page
        conventionURL = rq.get('https://animecons.com' + events[i]['href'].replace('-2023', '')).text
        conventionPage = bs(conventionURL, 'lxml')
        ev_url = conventionPage.select('.lead a[href*=google]')[0].attrs['href']

        #Get Convention Website from convention page
        ev_websiteURL = conventionPage.select('.box-body a[href*=AnimeCons]')[0].attrs['href'].split('?')[0]
        
        ## create obj with event info
        csvData.append({
            'column_01': ev_name,
            'column_02': ev_url,
            'column_03': ev_date,
            'column_04': ev_space,
            'column_05': ev_cityState,
            'column_06': ev_websiteURL
        })
    
    fieldnames = csvData[0].keys() #takes the whole array and fetches keys
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(csvData)

print('Done!')