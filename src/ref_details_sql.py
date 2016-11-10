import cPickle as pickle
import psycopg2 as pg2

from datetime import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup

def pickler_load(filename):
    with open(filename, 'r') as f:
        soln = pickle.load(f)
    return(soln)

def dash_check(value):
    if value != '-':
        return(int(value))
    else:
        return(0)

def team_name_check(value):
    teams = pickler_load('data/team_name_convert.pkl')

    if value in teams:
        return(teams[value])
    else:
        return(value)

'''
Load team name, team id and ref id conversion dicts
'''
team_id = pickler_load('data/team_dict.pkl')
ref_ids = pickler_load('data/ref_id_dict.pkl')
ref_code = pickler_load('data/ref_code_dict.pkl')

'''
Fetch all ref season details from MongoDB
'''
client = MongoClient()
db = client['penalty_card_pred']
ref_det = db['ref_season_detail']

'''
Create Postgres Table
'''
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

cur.execute('''
            DROP TABLE IF EXISTS ref_details;
            ''')
con.commit()

cur.execute('''
            CREATE TABLE
            ref_details(id SERIAL PRIMARY KEY,
                        match_date DATE,
                        h_team TEXT,
                        h_id INT,
                        h_score INT,
                        a_team TEXT,
                        a_id INT,
                        a_score INT,
                        single_yellow INT,
                        double_yellow INT,
                        red INT,
                        ref_name TEXT,
                        ref_id INT);
            ''')
con.commit()

raw_data = ref_det.find({})
for data in raw_data:
    soup = BeautifulSoup(data['details'], 'html.parser')

    match = soup.find_all('td', {'class': 'hell'})
    num_matches = len(match) / 8

    ref_name = ref_code[data['ref_code']]
    ref_id = ref_ids[ref_name]

    for i in xrange(num_matches):
        date = datetime.strptime(match[8 * i].text, '%d/%m/%Y')

        h_team = team_name_check(match[8 * i + 1].text)
        h_id = team_id[h_team]

        a_team = team_name_check(match[8 * i + 3].text)
        a_id = team_id[a_team]

        score = match[8 * i + 4].text.split(':')
        h_score = int(score[0])
        a_score = int(score[1])

        single_y = dash_check(match[8 * i + 5].text)
        double_y = dash_check(match[8 * i + 6].text)
        red = dash_check(match[8 * i + 7].text)

        match_det = {'match_date': date,
                     'h_team': h_team,
                     'h_id': h_id,
                     'h_score': h_score,
                     'a_team': a_team,
                     'a_id': a_id,
                     'a_score': a_score,
                     'single_yellow': single_y,
                     'double_yellow': double_y,
                     'red': red,
                     'ref_name': ref_name,
                     'ref_id': ref_id}

        cur.execute('''
                    INSERT INTO
                    ref_details(match_date,
                                h_team,
                                h_id,
                                h_score,
                                a_team,
                                a_id,
                                a_score,
                                single_yellow,
                                double_yellow,
                                red,
                                ref_name,
                                ref_id)
                    VALUES
                    (%(match_date)s,
                     %(h_team)s,
                     %(h_id)s,
                     %(h_score)s,
                     %(a_team)s,
                     %(a_id)s,
                     %(a_score)s,
                     %(single_yellow)s,
                     %(double_yellow)s,
                     %(red)s,
                     %(ref_name)s,
                     %(ref_id)s)
                    ''', match_det)

        con.commit()
