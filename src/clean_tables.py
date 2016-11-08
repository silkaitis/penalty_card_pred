import json

from os import listdir

def collect_tables(dir):
    return(listdir(dir))

def new_table_name(filename):
    file_loc = filename.rfind('.')
    return(filename[:file_loc] + '_c' + filename[file_loc::])

def table_load(dir, filename):
    with open(dir + filename, 'r') as f:
        return(json.load(f))

def clean_keys(data):
    soln = []
    for row in data:
        if row != {}:
            t_soln = {}
            for key, val in row.iteritems():
                key_loc = key.rfind('}') + 1
                new_key = key[key_loc::]
                t_soln[new_key] = val
            soln.append(t_soln)
    return(soln)

def store_json(data, filename, dir):
    with open(dir + filename, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    directory = 'data/epl_tables/'
    dir_c = 'data/epl_tables_c/'

    files = collect_tables(directory)
    c_files = [new_table_name(fin) for fin in files]

    for old, new in zip(files, c_files):
        data = table_load(directory, old)
        store_json(clean_keys(data), new, dir_c)
