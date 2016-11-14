import sqlalchemy as sqla
import pandas as pd
import psycopg2 as pg2
import numpy as np
import cPickle as pickle

from team_status_funcs import (search_backward,
                                    base_data_grab,
                                    base_roller_params,
                                    roller_type,
                                    sql_info)

from feature_eng import feature_eng

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

def rolling_status(df, away_id, home_id):
    rng = 3
    h_a_split = 9 #Change if new features are added to fixtures in postgres
    base_param = base_roller_params(list(df.columns))


    #Create dummy header for match so feature_eng.py functions properly
    match_sum = np.zeros(6)

    fields = base_param[:h_a_split]
    row_temp = search_backward(len(df) - 1, away_id, df, fields, rng)
    match_sum = np.append(match_sum, row_temp)

    fields = base_param[h_a_split::]
    row_temp = search_backward(len(df) - 1, home_id, df, fields, rng)
    match_sum = np.append(match_sum, row_temp)
    return(match_sum)

def team_history(team_id, loc):
    if loc == 'home':
        t_sel = 'h'
        col = 'hometeam_id'
    elif loc == 'away':
        t_sel = 'a'
        col = 'awayteam_id'

    con, cur = connect_psql()
    query = '''
            SELECT avg_goals_{0}
            FROM fixtures_history
            WHERE {1} = {2}
            '''.format(t_sel, col, team_id)
    cur.execute(query)
    data = cur.fetchone()
    con.close()
    return(np.array(data))

def build_match(away, home):
    '''
    Input:
        - away: away team name (STR)
        - home: home team name (STR)
    Output:
        - soln: prediction array (LIST)
    '''
    df = load_df('fixtures')

    away_id = team_id_sql(away)
    home_id = team_id_sql(home)

    match_raw = rolling_status(df, away_id, home_id)
    match_raw = np.append(match_raw, team_history(home_id, 'home'))
    match_raw = np.append(match_raw, team_history(away_id, 'away'))

    df = load_df('base_table')
    match_feat = pd.DataFrame(columns=df.columns)
    match_feat.loc[0] = match_raw
    return(match_feat)

def model_load(model):
    with open(model, 'r') as f:
        return(pickle.load(f))

def trim_df(df):
    to_drop = ['match_id',
                'index',
                'awayyellowcards',
                'awayredcards',
                'homeyellowcards',
                'homeredcards']
    return(df.drop(to_drop, axis=1))

def predict_match(away, home):
    match_feat = build_match(away, home)

    match_pred = feature_eng(match_feat)
    match_pred = trim_df(match_pred)

    model = model_load('model.pkl')

    pred = model.predict(match_pred)
    return(pred[0])
