from bs4 import BeautifulSoup
import pandas as pd
import settings
import requests
import datetime


def get_charts(chart="regional", country="global", recurrence="daily", date="latest"):
    """
    Returns a DataFrame with requested Spotify charts data.
    Args:
    chart (Chart Type)
    'regional' => Top 200 [default]
    'viral'    => Viral 50
    country (Country):
    'global' => Global chart [default]
    'br'     => Country chart (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)
    recurrence (Recurrence):
    'daily'  => Daily chart
    'weekly' => Weekly chart
    date (Date):
    'latest'     => Latest chart
    'yyyy-mm-dd' => Specific date, for 'daily' recurrence
    'yyyy-mm-dd--YYYY-MM-DD' => Specific week range (e.g. 2021-07-30--2021-08-06), for 'weekly' recurrence
    """

    param = {}

    """
    Chart Type:
    'regional' => Top 200
    'viral'    => Viral 50
    """
    param["chart"] = chart

    """
    Country:
    'global' => Global chart
    'br'     => Country chart (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)
    """
    param["country"] = country

    """
    Recurrence:
    'daily'  => Daily chart
    'weekly' => Weekly chart
    """
    param["recurrence"] = recurrence

    """
    Date:
    'latest'     => Latest chart
    'yyyy-mm-dd' => Specific date, for 'daily' recurrence
    'yyyy-mm-dd--YYYY-MM-DD' => Specific week range (e.g. 2021-07-30--2021-08-06), for 'weekly' recurrence
    """
    param["date"] = date

    #requesting the HTML
    headers = {'User-Agent': settings.USER_AGENT}
    html_text = requests.get(f"https://spotifycharts.com/{param['chart']}/{param['country']}/{param['recurrence']}/{param['date']}/", headers=headers).text
    
    soup = BeautifulSoup(html_text, 'lxml')
    soup.prettify()

    #getting songs info
    song_url = soup.find_all('td', class_='chart-table-image')
    song_position = soup.find_all('td', class_='chart-table-position')
    song_track = soup.find_all('td', class_='chart-table-track')
    song_streams = soup.find_all('td', class_='chart-table-streams')

    #constructing the dataframe with songs info
    df = pd.DataFrame()
    i=0
    for song in song_track:
        row_data = {}
        row_data['date'] = str(datetime.date.today())
        row_data['url'] = song_url[i].find('a')['href']
        row_data['img'] = song_url[i].find('img')["src"]
        row_data['position'] = song_position[i].text.replace('\n','')
        row_data['track'] = song.strong.text
        row_data['artist'] = song.span.text.replace('by','')
        row_data['streams'] = song_streams[i].text.replace('\n','')
        row_df = pd.DataFrame.from_records([row_data])
        df = pd.concat([df, row_df], ignore_index=True)
        i+=1

    #os.makedirs("./data", exist_ok=True)
    #df.to_csv(f"./data/spotifycharts_{param['chart']}_{param['country']}_{param['recurrence']}_{param['date']}.csv", sep=";", index=False)

    return df
