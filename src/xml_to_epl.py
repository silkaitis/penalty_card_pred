import psycopg2 as pg2
import cPickle as pickle

with open('data/xml_to_epl.pkl', 'r') as f:
    name_convert = pickle.load(f)

'''
Pull team_id from XMLsoccer
'''
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

teams = {}
cur.execute('''SELECT DISTINCT(HomeTeam), HomeTeam_Id
                FROM fixtures;''')

for val in cur.fetchall():
    if val[0] in name_convert:
        name = name_convert[val[0]]
    else:
        name = val[0]
    teams[name] = val[1]

'''
Store team / id dictionary in a pickle
'''
with open('data/team_dict.pkl', 'w') as f:
    pickle.dump(teams, f)

'''
Reformat dictionary for SQL insertion
'''
team_sql = []
for key, val in teams.iteritems():
    team_sql.append({'team_id': val, 'name': key})

cur.execute('''DROP TABLE IF EXISTS team_code''')

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
con.close()
