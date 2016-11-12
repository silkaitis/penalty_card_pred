import sqlalchemy as sqla
import pandas as pd
import sys

def search_backward_sum(start, team_id, data, field, rng):
    '''
    Input:
        - start: starting position in DataFrame (INT)
        - team_id: team id (INT)
        - data: fixture data (DataFrame)
        - field: DataFrame field in question without
                    'home' or 'away' included (STR)
        - rng: number of matches to sum over (INT)
    Output:
        - soln: sum of field over range (INT)
    '''
    away = 'away' + field
    home = 'home' + field
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

'''
Collect Official Team Names (Official as in from EPL website)
'''
engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
df = pd.read_sql_table('fixtures', engine)

base = ['awayteam_id',
        'awayteam',
        'hometeam_id',
        'hometeam',
        'match_id',
        'date',
        'season']
mvg_avg = ['homeyellow_sum',
           'awayyellow_sum']
total = base + mvg_avg

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

    a_id = df['awayteam_id'].loc[i]
    h_id = df['hometeam_id'].loc[i]

    row = base_data_grab(df.loc[i], base)
    row.append(search_backward_sum(i - 1, h_id, df, 'yellowcards', rng))
    row.append(search_backward_sum(i - 1, a_id, df, 'yellowcards', rng))

    df_sum.loc[j] = row
    
sys.stdout.write("-")
sys.stdout.flush()
sys.stdout.write("\n")
print(df_sum.head())
