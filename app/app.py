import psycopg2 as pg2
import seaborn as sns
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, jsonify
from src.pred_match import predict_match

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components

import StringIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/predictions', methods=['GET'])
def predictions():
    return render_template('predictions.html')

@app.route('/pred', methods=['POST'])
def match():
    teams = request.json
    home, away = teams['home'], teams['away']
    pred = predict_match(away, home)
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

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]

    plt.plot(x,y)
    plt.xlabel(vars['x'])
    plt.ylabel(vars['y'])
    plt.savefig(img, format='png')
    img.seek(0)

    binary = base64.b64encode(img.getvalue())
    plot_binary = 'data:image/png;base64, ' + binary
    return plot_binary
#      # generate some random integers, sorted
#      exponent = .7+random.random()*.6
#      dta = []
#      for i in range(50):
#      rnum = int((random.random()*10)**exponent)
#      dta.append(rnum)
#      y = sorted(dta)
#      x = range(len(y))
#      # generate Bokeh HTML elements
#      # create a `figure` object
#      p = figure(title='A Bokeh plot',
#      plot_width=500,plot_height=400)
#      # add the line
#      p.line(x,y)
#      # add axis labels
#      p.xaxis.axis_label = "time"
#      p.yaxis.axis_label = "size"
#      # create the HTML elements to pass to template
#      figJS,figDiv = components(p,CDN)
#     return render_template('league_stats.html', figJS=figJS, figDiv=figDiv)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050', threaded=True)
