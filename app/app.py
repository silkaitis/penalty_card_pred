import StringIO
import base64

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

    match = predict_match(away, home, int(ref))
    match.fillna(value=0, inplace=True)

    pred = model.predict(match)

    pred = clean_up(pred[0])

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

    df = load_df('trans_fix')

    img = StringIO.StringIO()
    import pdb; pdb.set_trace()
    plt.figure()
    hmap = sns.heatmap(pd.pivot_table(df,
                                        columns=vars['x'],
                                        index=vars['y'],
                                        values='yellowcards',
                                        aggfunc=np.mean))
    fig = hmap.get_figure()
    fig.savefig(img, format='png')
    img.seek(0)

    binary = base64.b64encode(img.getvalue())
    plot_binary = 'data:image/png;base64, ' + binary
    return plot_binary

def clean_up(data):
    soln = []
    for val in data:
        if val < 0:
            soln.append(0)
        else:
            soln.append(round(val, 2))
    return(soln)

if __name__ == '__main__':
    with open('model.pkl') as f:
        model = pickle.load(f)

    app.run(host='0.0.0.0', port='8081', threaded=True)
