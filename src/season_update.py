import datetime
import yaml

from pymongo import MongoClient
from xmlsoccer.xmlsoccer import XmlSoccer
from extract_data_funcs import historic_data, season_builder, ref_store

'''
Load API key and connect
'''
with open('src/key.yaml') as fin:
    keys = yaml.load(fin)

xmls = XmlSoccer(api_key=keys['XMLS_key'], use_demo=False)

'''
League Variables
'''
EPL = 'English Premier League'

seasons = ['1617']

fixture_fpath = 'data/epl_fixtures/'
table_fpath = 'data/epl_tables/'

'''
Extract league tables
'''
historic_data(league = EPL,
                seasons = seasons,
                fpath = table_fpath,
                api_call = 'table',
                api_conn = xmls)

'''
Extract league fixtures
'''
historic_data(league = EPL,
                seasons = seasons,
                fpath = fixture_fpath,
                api_call = 'fixtures',
                api_conn = xmls)

'''
Scrape ref data
'''
client = MongoClient()
db = client['penalty_card_pred']
ref_sum = db['ref_season_summary']
ref_det = db['ref_season_detail']

ref_store(2016, ref_sum, ref_det)

client.close()
