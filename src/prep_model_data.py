import pandas as pd
import psycopg2 as pg2

from rolling_team_status import rts

'''
Build rolling metric table (current set to sum metric)
'''
rts('fixtures_sum_test', 3)
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
Build base table with only labels and transformed data
'''
cur.execute(open('src/base_table.sql', 'r').read())
con.commit()
con.close()
print('Base Table Complete')
