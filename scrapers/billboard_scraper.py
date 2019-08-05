"""
This module contains scrapers designed to extract data from various webpages to build custom datasets.
Please note that many web scraping may be against the terms of use of some websites. Such websites will attempt to limit
web scraping, and may even block
"""

import requests, datetime, time, csv, sys
from bs4 import BeautifulSoup

datasets_folder = 'datasets'

def scrape_hot_100(min_date:tuple, max_date:tuple=None, data_file='billboard_hot_100.csv'):
    """
    Extracts data from the Billboard Hot 100 chart for a given range of dates.

    Parameters:
    min_date (tuple)        - The first week of the Billboard Hot 100 to extract data, formatted (mm, dd, yyyy).
                                ~ First week of Billboard Hot 100 was 1958-08-04
    max_date (tuple)        - The last week of the Billboard Hot 100 to extract data, formatted (mm, dd, yyyy).
                                ~ Most current week by default
    data_file (str)         - A .csv file name to store the extracted data; will be overwritten if it already exists.
                                ~ If the file does not end in '.csv', it will be appended to the file name
                                ~ 'billboard_hot_100.csv' by default

    Dataset Features:
    Position (int)          - The rank of the song in the current week
    Title (str)             - The song title
    Artist (str)            - The song artists
    Last Week (int)         - The rank of the song in the previous week
                                ~ Empty if the song was not on the Billboard Hot 100 the previous week
    Peak Position (int)     - The highest rank the song has reached on the Billboard Hot 100 until and including the current week
    Weeks on Chart (int)    - The number of weeks the song has been on the Billboard Hot 100 until and including the current week
    Chart Date (str)        - The date of the week the datapoint was collected from in the format mm-dd-yyyy
    """

    base_url = 'https://www.billboard.com/charts/hot-100'
    features = ['Position', 'Title', 'Artist', 'Last Week', 'Peak Position', 'Weeks on Chart', 'Chart Date']
    total_time, charts_fetched = 0, 0

    # Date range
    min_date = datetime.date(min_date[2], min_date[0], min_date[1])
    date = datetime.date.today() if not max_date else datetime.date(max_date[2], max_date[0], max_date[1])
    date += datetime.timedelta((12 - date.weekday()) % 7) # Gets next Saturday
    if date < min_date: return

    if data_file[-4:] != '.csv': data_file += '.csv'
    global datasets_folder
    with open(f'{datasets_folder}/{data_file}', mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, features)
        writer.writeheader()

        week_delta = datetime.timedelta(weeks=1)
        while date >= min_date:
            # Collect program metadata
            charts_fetched += 1
            time_interval = time.time_ns()

            # Get current Billboard Hot 100 page
            print('Fetching chart for week of', date.strftime('%m-%d-%Y'), '...', end=' ')
            sys.stdout.flush()
            try:
                page = requests.get('{url}/{date}'.format(url=base_url, date=date.strftime('%Y-%m-%d')))
                if not page:
                    print('an error has occurred!')
                    continue
            except requests.exceptions.ConnectionError:
                print('The connection was unexpectedly closed.')
                raise
            soup = BeautifulSoup(page.text, 'lxml')

            # Get date of Billboard chart week
            chart_date = soup.find('button', {'class': 'chart-detail-header__date-selector-button'}).contents[0].string.strip()
            chart_date = datetime.datetime.strptime(chart_date, '%B %d, %Y')
            date = datetime.date(chart_date.year, chart_date.month, chart_date.day) - week_delta # Not all chart weeks are based around Saturday

            # Collect song data for current week
            song_list = soup.find_all('div', {'class': 'chart-list-item'})
            song_data = []
            for song in song_list:
                song_info = dict.fromkeys(features)
                song_info['Chart Date'] = chart_date.strftime('%m-%d-%Y')
                song_info['Position'] = int(song['data-rank'])
                song_info['Title'] = song['data-title']
                song_info['Artist'] = song['data-artist']

                extra_info = song.find('div', {'class': 'chart-list-item__stats'})
                if extra_info is None: # For songs that are making their debut on the Billboard Hot 100
                    song_info['Last Week'] = None
                    song_info['Peak Position'] = song_info['Position']
                    song_info['Weeks on Chart'] = 1
                else: # For songs that have been on the Billboard Hot 100
                    last_week = extra_info.find('div', {'class': 'chart-list-item__last-week'}).string
                    song_info['Last Week'] = int(last_week) if last_week != '-' else None
                    song_info['Peak Position'] = int(extra_info.find('div', {'class': 'chart-list-item__weeks-at-one'}).string)
                    song_info['Weeks on Chart'] = int(extra_info.find('div', {'class': 'chart-list-item__weeks-on-chart'}).string)
                song_data.append(song_info)

            # Append data to CSV
            writer.writerows(song_data)

            # Update program metadata
            time_interval = (time.time_ns() - time_interval) * 10**-9
            total_time += time_interval
            print('done in', round(time_interval, 5), 'seconds')
            time.sleep(2)

    print('DONE; fetched', charts_fetched, 'week{s} of Billboard Hot 100 data in'.format(s='' if charts_fetched == 1 else 's'), round(total_time, 5), 'seconds.')
    return data_file

if __name__ == '__main__':
    pass