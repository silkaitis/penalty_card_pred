import sqlalchemy as sqla
import pandas as pd
import psycopg2 as pg2
import numpy as np

def shotsontar_shots(data):
    '''
    INPUT:
        - data: Pandas DataFrame
    OUTPUT:
        - soln: Pandas DataFrame
    '''
    soln = {'home_sots': (data.homeshots_sum3 / data.shotsontarget_sum3).values}
    return(pd.DataFrame(soln))

def feature_eng(data):
    '''
    INPUT:
        - data: Pandas DataFrame
    OUTPUT:
        - soln: Pandas DataFrame
    '''
    return(data)
