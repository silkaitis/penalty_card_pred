import psycopg2 as pg2

con = pg2.connect(database='pen_card', user='danius')
cur = con.cursor()

for p in ['home', 'away']:
    tbl = p + '_trans'
    cur.execute('''
                DROP TABLE IF EXISTS %s;
                ''' % pg2.extensions.AsIs(tbl))

    cur.execute('''
                CREATE TABLE {0}_trans AS
                    SELECT fixtures.{0}corners as corners,
                           fixtures.{0}fouls as fouls,
                           fixtures.{0}goals as goals,
                           fixtures.{0}goalsallowed as goalsallowed,
                           fixtures.{0}redcards as redcards,
                           fixtures.{0}yellowcards as yellowcards,
                           fixtures.{0}shots as shots,
                           fixtures.{0}shotsontarget as shotsontarget,
                           fixtures.{0}team as team,
                           fixtures.{0}team_id as team_id,
                           fixtures.season as season,
                           fixtures.match_id as match_id,
                           fixtures.date as date,
                           ref_details.ref_name as ref_name,
                           ref_details.ref_id as ref_id
                    FROM fixtures
                    LEFT JOIN ref_details ON ref_details.match_id = fixtures.match_id;
                '''.format(p))

    cur.execute('''
                ALTER TABLE {0}_trans
                ADD COLUMN loc TEXT
                DEFAULT '{0}';
                '''.format(p))
    con.commit()

cur.execute('''
            DROP TABLE IF EXISTS trans_fix;
            ''')

cur.execute('''
            CREATE TABLE trans_fix AS
                SELECT *
                FROM home_trans
                UNION
                SELECT *
                FROM away_trans;
            ''')
con.commit()
con.close()
