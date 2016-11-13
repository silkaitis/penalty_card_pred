import sys

import sqlalchemy as sqla
import pandas as pd
import numpy as np
import cPickle as pickle

from datetime import datetime
from src.team_status_funcs import (search_backward,
                                    base_data_grab,
                                    base_roller_params,
                                    roller_type,
                                    sql_info)

def rts(tbl_name, n_matches):
    '''
    Collect Official Team Names (Official as in from EPL website)
    '''
    engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
    df = pd.read_sql_table('fixtures', engine)

    '''
    Create lists for organizing data
    '''
    #Useful information per fixture for SQL and
    #match labels for prediction
    base = sql_info()

    h_a_split = 9 #Change if new features are added to fixtures in postgres
    base_param = base_roller_params(list(df.columns))
    rename_param = roller_type(base_param, '_sum' + str(n_matches))
    total = base + rename_param

    '''
    Save list of renamed parameters
    '''
    with open('renamed_params.pkl', 'w') as f:
        pickle.dump(rename_param, f)

    '''
    Create empty DataFrame and set moving sum range
    '''
    df_sum = pd.DataFrame(columns=total)
    rng = n_matches

    '''
    Setup progress toolbar
    '''
    step = 1
    toolbar_width = 40
    increment = len(df) / float(toolbar_width)

    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))

    '''
    Iterate through fixtures DataFrame
    and compute moving sum
    '''
    for j, i in enumerate(xrange(len(df) - 1, -1, -1)):
        test = int(increment * step)
        if j >= test and j < test + 1:
            sys.stdout.write("-")
            sys.stdout.flush()
            step += 1

        row = base_data_grab(df.loc[i], base)

        a_id = df['awayteam_id'].loc[i]
        fields = base_param[:h_a_split]
        row_temp = search_backward(i - 1, a_id, df, fields, rng)

        row = np.append(row, row_temp)

        h_id = df['hometeam_id'].loc[i]
        fields = base_param[h_a_split::]
        row_temp = search_backward(i - 1, h_id, df, fields, rng)

        row = np.append(row, row_temp)

        df_sum.loc[j] = row

    sys.stdout.write("-")
    sys.stdout.flush()
    sys.stdout.write("\n")

    '''
    Save DataFrame to Postgres
    '''
    df_sum.to_sql(tbl_name, engine, if_exists='replace')
