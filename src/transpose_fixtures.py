import psycopg2 as pg2

def team_selector(status, data):
    '''
    INPUT:
        - status ~ STR, home or away
        - data ~ TUPLE, query result
    OUTPUT:
        - soln ~ DICT, dictionary of team performance
    '''
    soln = {}

    if status == 'home':
        idx = 1
        soln['Loc'] = 'home'
    else:
        idx = 0
        soln['Loc'] = 'away'

    keys = ['Corners',
            'Fouls',
            'Goals',
            'RedCards',
            'Shots',
            'ShotsOnTarget',
            'Team',
            'Team_Id',
            'YellowCards',
            'Date',
            'HalfTimeGoals',
            'Id',
            'Ref_Id',
            'Ref',
            'Season']
    loc = [i + idx * 12 for i in xrange(9)] #Select upto date
    loc.extend([9, 10 + idx, 22, 23, 24, 21]) #Add date, halftimegoals, id, ref_id, ref, season

    for k, v in zip(keys, loc):
        soln[k] = data[v]

    return(soln)

'''
Create table for transposed fixture results
'''
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

cur.execute('''
            DROP TABLE IF EXISTS trans_fix;
            ''')
con.commit()

cur.execute('''
            CREATE TABLE
            trans_fix(Id INT,
                      Date DATE,
                      Fouls INT,
                      YellowCards INT,
                      RedCards INT,
                      Corners INT,
                      HalfTimeGoals INT,
                      Shots INT,
                      ShotsOnTarget INT,
                      Goals INT,
                      Team TEXT,
                      Team_Id INT,
                      Ref TEXT,
                      Ref_Id INT,
                      Loc TEXT,
                      Season INT)
            ''')
con.commit()

'''
Grab ref and fixture data from existing SQL tables
'''
cur.execute('''
            SELECT fixtures.*, ref_details.ref_id, ref_details.ref_name
            FROM fixtures
            JOIN ref_details ON ref_details.match_id = fixtures.id;
            ''')

matches = cur.fetchall()

for row in matches:
    for pos in ['home', 'away']:
        team = team_selector(pos, row)
        cur.execute('''
                    INSERT INTO
                    trans_fix(Id,
                              Date,
                              Fouls,
                              YellowCards,
                              RedCards,
                              Corners,
                              HalfTimeGoals,
                              Shots,
                              ShotsOnTarget,
                              Goals,
                              Team,
                              Team_Id,
                              Ref,
                              Ref_Id,
                              Loc,
                              Season)
                    VALUES
                    (%(Id)s,
                     %(Date)s,
                     %(Fouls)s,
                     %(YellowCards)s,
                     %(RedCards)s,
                     %(Corners)s,
                     %(HalfTimeGoals)s,
                     %(Shots)s,
                     %(ShotsOnTarget)s,
                     %(Goals)s,
                     %(Team)s,
                     %(Team_Id)s,
                     %(Ref)s,
                     %(Ref_Id)s,
                     %(Loc)s,
                     %(Season)s);
                     ''', team)
        con.commit()
con.close()
