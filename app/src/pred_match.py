import sqlalchemy as sqla
import pandas as pd
import psycopg2 as pg2
import numpy as np
import cPickle as pickle

from team_status_funcs import (search_backward,
                                    search_backward_ref,
                                    base_data_grab,
                                    base_roller_params,
                                    roller_type,
                                    sql_info)

from feature_eng import feature_eng

def connect_psql():
    con = pg2.connect(database='pen_card', user='danius')
    cur = con.cursor()
    return(con, cur)

def load_df(tbl_name):
    engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
    return(pd.read_sql_table(tbl_name, engine))

def rolling_status(df, away_id, home_id, ref):
    rng = 3
    h_a_split = 9 #Change if new features are added to fixtures in postgres
    base_param = base_roller_params(list(df.columns))

    #Create dummy header for match so feature_eng.py functions properly
    match_sum = np.zeros(6)

    fields = base_param[:h_a_split]
    row_temp = search_backward(len(df) - 1, away_id, df, fields, rng)
    match_sum = np.append(match_sum, row_temp / float(rng))

    fields = base_param[h_a_split::]
    row_temp = search_backward(len(df) - 1, home_id, df, fields, rng)
    match_sum = np.append(match_sum, row_temp / float(rng))

    #Grab ref yellows
    row_temp = search_backward_ref(len(df) - 1, ref, 'yellowcards', df, rng)
    match_sum = np.append(match_sum, row_temp / float(rng))

    #Grab ref reds
    row_temp = search_backward_ref(len(df) - 1, ref, 'redcards', df, rng)
    match_sum = np.append(match_sum, row_temp / float(rng))

    return(match_sum)

def update_ref(team, ref, df, data, loc):
    if loc == 'away':
        team_loc = 'awayteam_id'
        yellow = 'ref_avg_ya'
        red = 'ref_avg_ra'
    elif loc == 'home':
        team_loc = 'hometeam_id'
        yellow = 'ref_avg_yh'
        red = 'ref_avg_rh'

    soln = df[(df[team_loc] == team) & (df.ref_id == ref)]
    data[yellow] = soln[yellow].mean()
    data[red] = soln[red].mean()
    return(data)

def teams_not_paired(home_id, away_id, df):
    data = df[(df.hometeam_id == home_id)].mean()
    d_temp = df[(df.awayteam_id == away_id)].mean()

    labels = ['avg_corners_a', 'avg_fouls_a', 'avg_goals_a',
                'avg_goalsa_a', 'avg_red_a', 'avg_yellow_a',
                'avg_shots_a', 'avg_sot_a', 'ref_avg_ya',
                'ref_avg_ra', 'hth_ca', 'hth_fa', 'hth_ga',
                'hth_gaa', 'hth_ra', 'hth_sa', 'hth_sota',
                'hth_ya', 'hth_htga']
    data[labels] = d_temp[labels]
    return(data)

def team_history(home_id, away_id, ref, df_hist):
    data = df_hist[(df_hist.hometeam_id == home_id)
                & (df_hist.awayteam_id == away_id)]

    if len(data) == 0:
        data = teams_not_paired(home_id, away_id, df_hist)
        data = update_ref(home_id, ref, df_hist, data, 'home')
        data = update_ref(away_id, ref, df_hist, data, 'away')
        data.drop(['match_id',
                    'ref_id',
                    'hometeam_id',
                    'awayteam_id'], inplace=True)
    else:
        data = data.iloc[0]
        data = update_ref(home_id, ref, df_hist, data, 'home')
        data = update_ref(away_id, ref, df_hist, data, 'away')
        data.drop(['match_id',
                    'ref_id',
                    'hometeam_id',
                    'team_h',
                    'awayteam_id',
                    'team_a'], inplace=True)
    return(data)

def build_match(away_id, home_id, ref, df_hist, df_full, df_bt):
    '''
    Input:
        - away: away team name (STR)
        - home: home team name (STR)
    Output:
        - soln: prediction array (LIST)
    '''

    match_raw = rolling_status(df_full, away_id, home_id, ref)
    match_raw = np.append(match_raw, team_history(home_id, away_id, ref, df_hist))

    match_feat = pd.DataFrame(columns=df_bt.columns)
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

def predict_match(away, home, ref, df_hist, df_full, df_bt):
    match_feat = build_match(away, home, ref, df_hist, df_full, df_bt)
    match_pred = feature_eng(match_feat)
    match_pred = trim_df(match_pred)

    return(match_pred)
