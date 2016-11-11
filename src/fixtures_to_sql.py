import json
import os

import cPickle as pickle
import psycopg2 as pg2

def name_switch(team, name):
    if team in name:
        return(name[team])
    else:
        return(team)

'''
Manual comparison between XML and EPL names
'''
name_convert = {'Birmingham': 'Birmingham City',
                 'Blackburn': 'Blackburn Rovers',
                 'Bolton': 'Bolton Wanderers',
                 'Bradford': 'Bradford City',
                 'Charlton': 'Charlton Athletic',
                 'Coventry': 'Coventry City',
                 'Derby': 'Derby County',
                 'Hull': 'Hull City',
                 'Ipswich': 'Ipswich Town',
                 'Leeds': 'Leeds United',
                 'Leicester': 'Leicester City',
                 'Man City': 'Manchester City',
                 'Man United': 'Manchester United',
                 'Newcastle': 'Newcastle United',
                 'Norwich': 'Norwich City',
                 'QPR': 'Queens Park Rangers',
                 'Sheffield United': 'Sheff Utd',
                 'Stoke': 'Stoke City',
                 'Swansea': 'Swansea City',
                 'Tottenham': 'Tottenham Hotspur',
                 'West Brom': 'West Bromwich Albion',
                 'West Ham': 'West Ham United',
                 'Wigan': 'Wigan Athletic',
                 'Wolves': 'Wolverhampton Wanderers'}

with open('data/xml_to_epl.pkl', 'w') as f:
    pickle.dump(name_convert, f)
'''
Create table for fixture results
'''
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

cur.execute('''
            DROP TABLE IF EXISTS fixtures;
            ''')
con.commit()

cur.execute('''
            CREATE TABLE
            fixtures(AwayCorners INT,
                     AwayFouls INT,
                     AwayGoals INT,
                     AwayRedCards INT,
                     AwayShots INT,
                     AwayShotsOnTarget INT,
                     AwayTeam TEXT,
                     AwayTeam_Id INT,
                     AwayYellowCards INT,
                     Date DATE,
                     HalfTimeAwayGoals INT,
                     HalfTimeHomeGoals INT,
                     HomeCorners INT,
                     HomeFouls INT,
                     HomeGoals INT,
                     HomeRedCards INT,
                     HomeShots INT,
                     HomeShotsOnTarget INT,
                     HomeTeam TEXT,
                     HomeTeam_Id INT,
                     HomeYellowCards INT,
                     Season INT,
                     Id INT PRIMARY KEY)
            ''')
con.commit()

dir = 'data/epl_fixtures/'
files = os.listdir(dir)
for fin in files:
    with open(dir + fin, 'r') as f:
        matches = json.load(f)

    print('File: {}'.format(fin))

    loc = fin.find('_') + 1
    season = fin[loc:loc+2]

    for match in matches:
        if match != {}:
            if fin == 'fixtures_0708.json':
                match['AwayFouls'] = -1
                match['HomeFouls'] = -1
                match['HalfTimeAwayGoals'] = -1
                match['HalfTimeHomeGoals'] = -1
            match['Season'] = season
            match['AwayTeam'] = name_switch(match['AwayTeam'], name_convert)
            match['HomeTeam'] = name_switch(match['HomeTeam'], name_convert)
            cur.execute('''
                        INSERT INTO
                        fixtures(AwayCorners,
                                 AwayFouls,
                                 AwayGoals,
                                 AwayRedCards,
                                 AwayShots,
                                 AwayShotsOnTarget,
                                 AwayTeam,
                                 AwayTeam_Id,
                                 AwayYellowCards,
                                 Date,
                                 HalfTimeAwayGoals,
                                 HalfTimeHomeGoals,
                                 HomeCorners,
                                 HomeFouls,
                                 HomeGoals,
                                 HomeRedCards,
                                 HomeShots,
                                 HomeShotsOnTarget,
                                 HomeTeam,
                                 HomeTeam_Id,
                                 HomeYellowCards,
                                 Season,
                                 Id)
                        VALUES
                        (%(AwayCorners)s,
                         %(AwayFouls)s,
                         %(AwayGoals)s,
                         %(AwayRedCards)s,
                         %(AwayShots)s,
                         %(AwayShotsOnTarget)s,
                         %(AwayTeam)s,
                         %(AwayTeam_Id)s,
                         %(AwayYellowCards)s,
                         %(Date)s,
                         %(HalfTimeAwayGoals)s,
                         %(HalfTimeHomeGoals)s,
                         %(HomeCorners)s,
                         %(HomeFouls)s,
                         %(HomeGoals)s,
                         %(HomeRedCards)s,
                         %(HomeShots)s,
                         %(HomeShotsOnTarget)s,
                         %(HomeTeam)s,
                         %(HomeTeam_Id)s,
                         %(HomeYellowCards)s,
                         %(Season)s,
                         %(Id)s)
                         ''', match)
            con.commit()

con.close()
