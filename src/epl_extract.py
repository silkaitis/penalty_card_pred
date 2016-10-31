import datetime
import yaml

from xmlsoccer.xmlsoccer import XmlSoccer
from extract_data_funcs import historic_data, season_builder

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

seasons = season_builder(0, 16)

fixture_fpath = 'data/epl_fixtures/'
table_fpath = 'data/epl_tables/'

# '''
# Extract league tables
# '''
# historic_data(league = EPL,
#                 seasons = seasons,
#                 fpath = table_fpath,
#                 api_call = 'table',
#                 api_conn = xmls)

'''
Extract league fixtures
'''
historic_data(league = EPL,
                seasons = seasons,
                fpath = fixture_fpath,
                api_call = 'fixtures',
                api_conn = xmls)
