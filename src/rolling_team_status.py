import sqlalchemy as sqla
import pandas as pd
import sys

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
    return(soln)

def base_roller_params(names):
    to_drop = [24, 23, 21, 20, 10, 9, 8, 7]
    for d in to_drop:
        names.pop(d)
    return(names)

def roller_type(names, met):
    return([val + met for val in names])

'''
Collect Official Team Names (Official as in from EPL website)
'''
engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
df = pd.read_sql_table('fixtures', engine)

'''
Create lists for organizing data
'''
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

base_param = base_roller_params(list(df.columns))
rename_param = roller_type(base_param, '_sum')
total = base + rename_param

df_sum = pd.DataFrame(columns=total)
rng = 3

# setup toolbar
step = 1
toolbar_width = 40
increment = len(df) / float(toolbar_width)

sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1))

for j, i in enumerate(xrange(len(df) - 1, -1, -1)):
    test = int(increment * step)
    if j >= test and j < test + 1:
        sys.stdout.write("-")
        sys.stdout.flush()
        step += 1

    row = base_data_grab(df.loc[i], base)
    for item in base_param:
        if item.find('away') != -1:
            t_id = df['awayteam_id'].loc[i]
        elif item.find('home') != -1:
            t_id = df['hometeam_id'].loc[i]

        row.append(search_backward_sum(i - 1, t_id, df, item, rng))

    df_sum.loc[j] = row

sys.stdout.write("-")
sys.stdout.flush()
sys.stdout.write("\n")

df_sum.to_sql('fixtures_sum', engine)
