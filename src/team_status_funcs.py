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

    idx = 0
    soln = np.zeros(len(fields))
    while idx < rng:
        if start == -1:
            return(soln)

        if (data['awayteam_id'].loc[start] == team_id):
            soln += data[away].loc[start]
            idx += 1
        elif (data['hometeam_id'].loc[start] == team_id):
            soln += data[home].loc[start]
            idx += 1

        start -= 1
    return(soln)

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
    to_drop = [24, 23, 21, 20, 10, 8, 7]
    for d in to_drop:
        names.pop(d)
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
