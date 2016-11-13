import sqlalchemy as sqla
import pandas as pd
import cPickle as pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from feature_eng import feature_eng

engine = sqla.create_engine('postgresql+psycopg2://danius@localhost/pen_card')
df = pd.read_sql_table('base_table', engine)

'''
Transform base table into model table
'''
df_trans = feature_eng(df)

labels = ['awayyellowcards',
          'awayredcards',
          'homeyellowcards',
          'homeredcards']

y = df_trans[labels]

labels.append('index')
labels.append('match_id')
X = df_trans.drop(labels, axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = RandomForestRegressor(n_jobs = -1)
model.fit(X_train, y_train)
print(model.predict(X_test))

with open('app/model.pkl', 'w') as f:
    pickle.dump(model, f)
