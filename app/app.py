import StringIO
import base64
import math

import cPickle as pickle
import psycopg2 as pg2
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from flask import Flask, render_template, request, jsonify
from src.pred_match import predict_match, load_df


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/author', methods=['GET'])
def author():
    return render_template('author.html')

@app.route('/pred', methods=['POST'])
def match():
    teams = request.json
    home, away, ref = teams['home'], teams['away'], teams['ref']

    match = predict_match(int(away),
                          int(home),
                          int(ref),
                          df_hist,
                          df_full,
                          df_bt)
    match.fillna(value=0, inplace=True)

    pred = model.predict(match)
    pred = cards(pred[0])

    return jsonify({'home': home,
                    'home_yellow': pred[2],
                    'home_red': pred[3],
                    'away': away,
                    'away_yellow': pred[0],
                    'away_red': pred[1]})

@app.route('/league_stats', methods=['GET'])
def league_stats():
    return render_template('league_stats.html')

@app.route('/graph_binary', methods=['POST'])
def graph():
    vars = request.json

    img = StringIO.StringIO()

    plt.figure()
    p_table = pd.pivot_table(df_trans,
                             columns=vars['x'],
                             index=vars['y'],
                             values=vars['v'],
                             aggfunc='mean')
    hmap = sns.heatmap(p_table.sort_index(ascending = False))

    hmap.set_title('Average ' + vars['vn'])
    hmap.set_xlabel(vars['xn'])
    hmap.set_ylabel(vars['yn'])
    hmap.set_yticklabels(hmap.get_ymajorticklabels(), rotation=0)
    hmap.set_xticklabels(hmap.get_xmajorticklabels(), rotation=90)

    fig = hmap.get_figure()
    fig.savefig(img, format='png')
    img.seek(0)

    binary = base64.b64encode(img.getvalue())
    plot_binary = 'data:image/png;base64, ' + binary
    return plot_binary

@app.route('/graph_binary_tc', methods=['POST'])
def graph_tc():
    vars = request.json

    img = StringIO.StringIO()

    sns.set(style='whitegrid')

    g = sns.PairGrid(df_sub.sort_values(vars['x'], ascending=False),
                        x_vars=[vars['x'], vars['y'], vars['v']],
                        y_vars=['team'],
                        size=5,
                        aspect=.45)
    g.map(sns.stripplot,
            size=10,
            orient="h",
            palette=sns.cubehelix_palette(20, start=.5, rot=-.75, reverse=True),
            edgecolor="gray")

    titles = [vars['xn'], vars['yn'], vars['vn']]
    for ax, title in zip(g.axes.flat, titles):
        ax.set(xlabel=title, title=title, ylabel='')

        for tick in ax.get_xticklabels():
            tick.set_rotation(90)

        ax.xaxis.grid(False)
        ax.yaxis.grid(True)

    sns.despine(left=True, bottom=True)
    g.savefig(img, format='png')
    img.seek(0)

    binary = base64.b64encode(img.getvalue())
    plot_binary = 'data:image/png;base64, ' + binary
    return plot_binary

def poisson_prob(u, n):
    soln = (np.exp(-u) * pow(u, n)) / math.factorial(n)
    return(soln)

def cards(y_pred):
    soln = [0] * len(y_pred)

    for k, val in enumerate(y_pred):
        temp = 0
        for i in xrange(10):
            calc = poisson_prob(val, i)
            if calc > temp:
                soln[k] = i
                temp = calc
    return(soln)

if __name__ == '__main__':
    with open('model.pkl') as f:
        model = pickle.load(f)

    df_hist = load_df('fixtures_history')
    df_full = load_df('fixtures_full')
    df_bt = load_df('base_table')
    df_trans = load_df('trans_fix')

    df_sub = df_trans[df_trans.season == 16].groupby('team').mean()
    df_sub = df_sub.reset_index()

    app.run(host='0.0.0.0', port='8081', threaded=True)
