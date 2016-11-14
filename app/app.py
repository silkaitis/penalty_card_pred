import psycopg2 as pg2

from flask import Flask, render_template, request, jsonify
from pred_match import predict_match

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050', threaded=True)
