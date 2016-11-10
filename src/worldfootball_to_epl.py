import cPickle as pickle
import psycopg2 as pg2
import sqlalchemy as sqla
import pandas as pd

from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient()
db = client['penalty_card_pred']
ref_det = db['ref_season_detail']

ref_raw = ref_det.find({})
alt_names = set()
for ref in ref_raw:
    soup = BeautifulSoup(ref['details'], 'html.parser')

    match = soup.find_all('td', {'class': 'hell'})
    num_matches = len(match) / 8

    for i in xrange(num_matches):
        alt_names.add(match[8 * i + 1].text)
        alt_names.add(match[8 * i + 3].text)

with open('data/alt_team_names.pkl', 'w') as f:
    pickle.dump(alt_names, f)

'''
Collect Official Team Names (Official as in from EPL website)
'''
engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
df = pd.read_sql_table('team_code', engine)
epl_names = set(df.sort_values(by='name').name.values)

'''
Create dictionary that converts team name from worldfootball.net
to match EPL names
'''
conv_dict = {}
for val in sorted(alt_names):
    if val not in epl_names:
        clean_name = str(val).replace('AFC', '')
        clean_name = clean_name.replace('FC', '')
        clean_name = clean_name.replace('City', '')
        clean_name = clean_name.replace(' ', '')
        conv_dict[val] = clean_name
conv_dict['Sheffield United'] = 'Sheff Utd'

with open('data/team_name_convert.pkl', 'w') as f:
    pickle.dump(conv_dict, f)
