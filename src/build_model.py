import sqlalchemy as sqla
import pandas as pd
import cPickle as pickle

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

'''
Load data base table
'''
engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
df = pd.read_sql_table('base_table', engine)

labels = ['awayyellowcards',
          'awayredcards',
          'homeyellowcards',
          'homeredcards']

y = df[labels]

labels.append('index')
labels.append('match_id')
X = df.drop(labels, axis=1)

'''
Split data into training and test sets
'''
X_train, X_test, y_train, y_test = train_test_split(X, y)

model = LinearRegression(n_jobs=-1)
model.fit(X_train, y_train)

with open('app/model.pkl', 'w') as f:
    pickle.dump(model, f)
