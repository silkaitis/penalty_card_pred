import json
import yaml
import datetime
import os
import pickle

from time import sleep

def season_builder(start, finish):
    '''
    Input: start ~ first year of first season available; INT
           finish ~ first year of last season available; INT
    Output: soln ~ list of two year code of season; LIST
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

def do_i_wait():
    '''
    Input: None
    Output: None
    Note: Function waits one hour between calls
            to adhere to API rules
    '''
    if not os.path.isfile('data/last_call.p'):
        pickle.dump(datetime.datetime.now(),
                    open('data/last_call.p', 'wb'))
        return
    else:
        api_time = pickle.load(open('data/last_call.p', 'r'))
        d_time = (datetime.datetime.now - api_time).seconds
        if d_time < 3600:
            sleep(3600 - d_time)
            return
        else:
            return


def historic_data(league, seasons, fpath, api_call, api_conn):
    '''
    Input: league ~ name of league; STR
           seasons ~ two year code of season; LIST
           fpath ~ file path to save data; STR
           api_call ~ fixtures or table; STR
           api_conn ~ XmlSoccer method; class
           api_time ~ time of last API call; datetime
    Output: None
    '''
    if api_call == 'fixtures':
        method = 'GetHistoricMatchesByLeagueAndSeaon'
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

        api_time = datetime.datetime.now()

        file = fpath + prefix + sea + '.json'
        with open(file, 'w') as fin:
            json.dump(fixtures, fin)

        print('Season {} {} saved.'.format(sea, api_call))
