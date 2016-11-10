import psycopg2 as pg2
import cPickle as pickle

from pymongo import MongoClient

'''
Pull all ref names from MongoDB and clean
'''

client = MongoClient()
db = client['penalty_card_pred']
ref_det = db['ref_season_detail']

ref_raw = ref_det.distinct('ref_code')

refs = {}
ref_codes = {}
i = 100
for ref in ref_raw:
    loc = ref.rfind('_2')
    name = ref[:loc].replace('_', ' ').title()
    ref_codes[ref] = name
    if name not in refs:
        refs[name] = i
        i += 1

with open('data/ref_code_dict.pkl', 'w') as f:
    pickle.dump(ref_codes, f)

with open('data/ref_id_dict.pkl', 'w') as f:
    pickle.dump(refs, f)

ref_sql = []
for key, val in refs.iteritems():
    ref_sql.append({'ref_id': val, 'ref_name': key})

'''
Build ref code table in SQL
'''
con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

cur.execute('''
            DROP TABLE IF EXISTS ref_code;
            ''')
con.commit()

cur.execute('''
            CREATE TABLE
            ref_code(ref_id INTEGER PRIMARY KEY, ref_name TEXT);
            ''')
con.commit()

cur.executemany('''
                INSERT INTO
                ref_code(ref_id, ref_name)
                VALUES
                (%(ref_id)s, %(ref_name)s);
                ''', ref_sql)
con.commit()
con.close()
