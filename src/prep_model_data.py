import pandas as pd
import psycopg2 as pg2

from rolling_team_status import rts

'''
Build rolling metric table (current set to sum metric)
'''
rts('fixtures_sum', 3)
print('Rolling Metric Table Complete')

'''
Build historical metric table (currently only goals)
'''
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

cur.execute(open('src/historical_query.sql', 'r').read())
con.commit()
print('Historical Metric Table Complete')

'''
Build model table with only labels and predictors
'''
cur.execute(open('src/model_table.sql', 'r').read())
con.commit()
con.close()
print('Model Table Complete')
