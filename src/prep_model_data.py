import pandas as pd
import psycopg2 as pg2

from rolling_team_status import rts
from datetime import datetime

now = datetime.now()
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

'''
Add referee to fixtures table
'''
cur.execute(open('src/add_ref_to_fixtures.sql', 'r').read())
con.commit()

'''
Build rolling metric table (current set to sum metric)
'''
rts('fixtures', 3, 'avg')
print('Rolling Metric Table Complete')

'''
Build historical metric table (currently only goals)
'''
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
print(datetime.now() - now)
