import sqlalchemy as sqla
import pandas as pd
import psycopg2 as pg2
import numpy as np

from team_status_funcs import (search_backward,
                                    base_data_grab,
                                    base_roller_params,
                                    roller_type,
                                    sql_info)

def connect_psql():
    con = pg2.connect(database='pen_card', user='danius')
    cur = con.cursor()
    return(con, cur)

def team_id_sql(name):
    con, cur = connect_psql()
    query = '''SELECT team_id
                FROM team_code
                WHERE name = '{}';'''.format(name)
    cur.execute(query)
    team_id = cur.fetchone()[0]
    con.close()
    return(team_id)

def load_df(tbl_name):
    engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
    return(pd.read_sql_table(tbl_name, engine))

def build_match(away, home):
    '''
    Input:
        - away: away team name (STR)
        - home: home team name (STR)
    Output:
        - soln: prediction array (LIST)
    '''

    df = load_df('fixtures')

    rng = 3
    h_a_split = 9 #Change if new features are added to fixtures in postgres
    base_param = base_roller_params(list(df.columns))

    away_id = team_id_sql(away)
    home_id = team_id_sql(home)

    #Create dummy header for match so feature_eng.py functions properly
    match_sum = np.array([0, away_id, away, home_id, home, 0, 0, 0])

    fields = base_param[:h_a_split]
    row_temp = search_backward(len(df) - 1, away_id, df, fields, rng)

    match_sum = np.append(match_sum, row_temp)

    fields = base_param[h_a_split::]
    row_temp = search_backward(len(df) - 1, home_id, df, fields, rng)

    match_sum = np.append(match_sum, row_temp)
    print(base_param)
    return(match_sum)

print build_match('Manchester United', 'Manchester City')
