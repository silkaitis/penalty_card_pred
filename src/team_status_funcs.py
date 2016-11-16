import numpy as np
import pandas as pd

def sql_info():
    base = ['awayteam_id',
            'awayteam',
            'hometeam_id',
            'hometeam',
            'match_id',
            'date',
            'season',
            'awayyellowcards',
            'awayredcards',
            'homeyellowcards',
            'homeredcards']
    return(base)

def search_backward(start, team_id, data, fields, rng):
    '''
    Input:
        - start: starting position in DataFrame (INT)
        - team_id: team id (INT)
        - data: fixture data (DataFrame)
        - fields: match metrics to sum over (LIST)
        - rng: number of matches to sum over (INT)
    Output:
        - soln: sum of field over range (INT)
    '''
    if fields[0].find('away') != -1:
        away = fields
        home = [val.replace('away', 'home') for val in fields]
    elif fields[0].find('home') != -1:
        away = [val.replace('home', 'away') for val in fields]
        home = fields

    ref = data['ref_id'].loc[start]

    idx = 0
    soln = np.zeros(len(fields))
    pts = 0
    ref_yellow = 0
    ref_idx = 0
    while idx < rng:
        if start == -1:
            return(np.append(soln, [pts]))


        if (data['awayteam_id'].loc[start] == team_id):
            soln += data[away].loc[start]
            pts += win_loss(data[away].loc[start])
            idx += 1

        elif (data['hometeam_id'].loc[start] == team_id):
            soln += data[home].loc[start]
            pts += win_loss(data[home].loc[start])
            idx += 1

        start -= 1

    return(np.append(soln, [pts]))

def search_backward_ref(start, ref, card, data, rng):
    idx = 0
    ref_yellow = 0
    while idx < rng:
        if start == -1:
            return(ref_yellow)

        if (data['ref_id'].loc[start] == ref):
            ref_yellow += data['away' + card].loc[start]
            ref_yellow += data['home' + card].loc[start]
            idx += 1

        start -= 1

    return(ref_yellow)

def search_backward_df(start, team_id, data, fields, rng):
    start += 1
    if fields[0].find('away') != -1:
        away = fields
        home = [val.replace('away', 'home') for val in fields]
    elif fields[0].find('home') != -1:
        away = [val.replace('home', 'away') for val in fields]
        home = fields
    pts = 0
    dt = data.iloc[start].date
    df_temp = data[((data.hometeam_id == team_id)
                    | (data.awayteam_id == team_id))
                    & (data.date < dt)][:rng].sort_values(by='date', ascending=False)[:3]

    soln = np.zeros(len(fields))
    for i in xrange(rng):
        if df_temp.iloc[i].hometeam_id == team_id:
            soln += df_temp[home].iloc[i]
            pts += win_loss(data[home].loc[start])
        elif df_temp.iloc[i].awayteam_id == team_id:
            soln += df_temp[away].iloc[i]
            pts += win_loss(data[away].loc[start])

    return(np.append(soln, [pts]))


def win_loss(data):
    '''
    Input:
        - data: DataFrame row (DF)
    Output:
        - soln: points earned over the previous matches (INT)
    '''
    if data.keys()[0].find('away') != -1:
        tag = 'away'
    elif data.keys()[0].find('home') != -1:
        tag = 'home'

    goals = data[tag + 'goals']
    goalsallowed = data[tag + 'goalsallowed']

    if goals > goalsallowed:
        return(3)
    elif goals == goalsallowed:
        return(1)
    else:
        return(0)

def search_backward_sum(start, team_id, data, field, rng):
    '''
    Input:
        - start: starting position in DataFrame (INT)
        - team_id: team id (INT)
        - data: fixture data (DataFrame)
        - field: match metric to sum over (STR)
        - rng: number of matches to sum over (INT)
    Output:
        - soln: sum of field over range (INT)
    '''
    if field.find('away') != -1:
        away = field
        home = field.replace('away', 'home')
    elif field.find('home') != -1:
        away = field.replace('home', 'away')
        home = field

    idx = 0
    soln = 0
    while idx < rng:
        if start == -1 and idx != 0:
            return(soln)
        elif start == -1 and idx == 0:
            return(0)

        if (data['awayteam_id'].loc[start] == team_id):
            soln += data[away].loc[start]
            idx += 1
        elif (data['hometeam_id'].loc[start] == team_id):
            soln += data[home].loc[start]
            idx += 1

        start -= 1
    return(soln)

def base_data_grab(data, base):
    '''
    Input:
        - data: single fixture (DataFrame row)
        - base: uneditted fields to collect (LIST of STRs)
    Output:
        - soln: list of fields (LIST)
    '''
    soln = []
    for b in base:
        soln.append(data[b])
    return(np.array(soln))

def base_roller_params(names):
    '''
    Input:
        - names: column names in DataFrame (LIST)
    Output:
        - names: reduced list of column names for
                    moving metric calculation (LIST)
    '''

    #Change to_drop if new features are added to fixtures in postgres
    to_drop = ['match_id', 'awayteam', 'awayteam_id',
                'date', 'hometeam', 'hometeam_id',
                'season', 'ref_id']
    for d in to_drop:
        names.remove(d)
    return(names)

def roller_type(names, met):
    '''
    Input:
        - names: reduced list of column names for
                    moving metric calculation (LIST)
        - met: metric being calculated; such as sum or avg (STR)
    Output:
        - names: new column names (LIST)
    '''
    return([val + met for val in names])
