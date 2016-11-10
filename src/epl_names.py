import psycopg2 as pg2
import cPickle as pickle

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

'''
Scrape list of all teams that were in the EPL
'''
driver = webdriver.Chrome('/Users/danius/anaconda2/selenium/webdriver/chromedriver')
url = 'https://www.premierleague.com/stats/head-to-head'
xpath = '//*[@data-tab-index="1"]'

driver.get(url)
sleep(2)
driver.execute_script('window.scrollTo(0, 300);')
driver.find_element_by_xpath(xpath).click()
sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.close()

'''
Create team_id dictionary
'''
team_cards = soup.find_all('div', {'class' : 'team-card'})
teams = {}
for i, team in enumerate(team_cards):
    teams[team.p.text] = i

'''
Store team / id dictionary in a pickle
'''
with open('team_dict.pkl', 'w') as f:
    pickle.dump(teams, f)

'''
Reformat dictionary for SQL insertion
'''
team_sql = []
for key, val in teams.iteritems():
    team_sql.append({'team_id': val, 'name': key})

'''
Create team id table in SQL database
'''
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

cur.execute('''
            CREATE TABLE team_code(team_id INTEGER PRIMARY KEY, name TEXT);
            ''')

con.commit()

cur.executemany('''
                INSERT INTO
                team_code(team_id, name)
                VALUES
                (%(team_id)s, %(name)s);
                ''', team_sql)

con.commit()
