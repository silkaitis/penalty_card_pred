import json
import yaml
import datetime
import os
import sys
import pickle

from time import sleep

def season_builder(start, finish):
    '''
    Input:
        - start: first year of first season available (INT)
        - finish: first year of last season available (INT)
    Output:
        - soln: list of two year code of season (LIST)

    Example:
        start = 1
        end = 3
        soln = ['0102', '0203', '0304']
    '''
    soln = []
    for yr in range(start, finish+1):
        if yr < 9:
            sea = '0' + str(yr) + '0' + str(yr + 1)
        elif yr == 9:
            sea = '0910'
        else:
            sea = str(yr) + str(yr + 1)
        soln.append(sea)
    return(soln)

def sleep_progress(length):
    '''
    Input:
        - length: time in seconds to wait till next API call (INT)
    Output:
        - None
    '''
    toolbar_width = 40

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    increment = length / float(toolbar_width)
    for i in xrange(toolbar_width):
        sleep(increment)
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("\n")

def call_time():
    '''
    Input:
        - None
    Output:
        - None
    Store current time in a pickle file
    '''
    pickle.dump(datetime.datetime.now(), open('data/last_call.p', 'wb'))

def do_i_wait():
    '''
    Input:
        - None
    Output:
        - None
    Decide whether to wait one hour between calls to adhere to API rules
    '''
    api_wait = 3601

    if not os.path.isfile('data/last_call.p'):
        call_time()
        return
    else:
        api_time = pickle.load(open('data/last_call.p', 'r'))
        d_time = (datetime.datetime.now() - api_time).seconds
        delta = api_wait - d_time

        if d_time < api_wait:
            print('Waiting on API: {} seconds'.format(delta))
            sleep_progress(delta)

        return


def historic_data(league, seasons, fpath, api_call, api_conn):
    '''
    Input:
        - league: name of league (STR)
        - seasons: two year code of season (LIST)
        - fpath: file path to save data (STR)
        - api_call: fixtures or table (STR)
        - api_conn: XmlSoccer method (class)
    Output:
        - None
    Exports historical season data to JSON file
    '''
    if api_call == 'fixtures':
        method = 'GetHistoricMatchesByLeagueAndSeason'
        prefix = 'fixtures_'
    elif api_call == 'table':
        method = 'GetLeagueStandingsBySeason'
        prefix = 'table_'
    else:
        print('Need to select fixtures or table')
        return

    for sea in seasons:
        do_i_wait()

        fixtures = api_conn.call_api(method=method,
                                        seasonDateString=sea,
                                        league=league)

        call_time()

        file = fpath + prefix + sea + '.json'
        with open(file, 'w') as fin:
            json.dump(fixtures, fin)

        print('Season {} {} saved.\n'.format(sea, api_call))
