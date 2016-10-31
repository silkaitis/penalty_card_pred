import requests

from pymongo import MongoClient
from bs4 import BeautifulSoup

def url_builder(yr1, yr2):
    base_url = 'http://www.worldfootball.net/referees/eng-premier-league-'
    end_url = '/1/'
    return(base_url + str(yr1) + '-' + str(yr2) + end_url)

'''
Initialize MongoDB
'''
client = MongoClient()
db = client['penalty_card_pred']
ref_sum = db['ref_season_summary']
ref_det = db['ref_season_detail']

base_url = 'http://www.worldfootball.net'
start_yr = 2000
end_yr = 2016

for yr in xrange(start_yr, end_yr + 1):
    '''
    Scrape referee summary table per season
    '''
    url = url_builder(yr, yr + 1)
    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find_all('table', {'class': 'standard_tabelle'})

    ref_sum.insert_one({'season': str(yr), 'table': str(table[0])})
    print('Season {}'.format(yr))
    
    '''
    Scrape referee season details table
    '''
    table_names = table[0].find_all('a')
    for name in table_names:
        ref_url = str(name.get('href'))
        if ref_url.find('premier') != -1:
            ref_code = ref_url.split('/')[2].replace('-', '_')
            print('Ref: {}'.format(ref_code))
            ref_code += '_' + str(yr)

            req_detail = requests.get(base_url + ref_url)
            soup_ref = BeautifulSoup(req_detail.content, 'html.parser')
            ref_table = soup_ref.find_all('table', {'class': 'standard_tabelle'})

            ref_det.insert_one({'ref_code': ref_code, 'details': str(ref_table[0])})

client.close()
