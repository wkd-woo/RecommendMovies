import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
import seaborn as sns
from sklearn.linear_model import Lasso
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform as sp_rand
import pickle
import os
import warnings

currentpath = os.getcwd()

warnings.filterwarnings('ignore')

# DB 연결
"""
connToRating = pymysql.connect(host="localhost", user="root", password="1234",
                      db="rating_data", charset="utf8")
cursor = connToRating.cursor(pymysql.cursors.DictCursor)

query = "SELECT * FROM ratings"
cursor.execute(query)

ratings = pd.read_sql(query, connToRating)
"""
ratings = pd.read_csv('analysisapp/data/ratings.csv')
my_ratings = pd.read_csv('analysisapp/data/my_ratings_input.csv')
movies = pd.read_csv('analysisapp/data/movies.csv')
with open('analysisapp/data/genres.p', 'rb') as f:
    genres = pickle.load(f)
genres = pd.read_pickle('analysisapp/data/genres.p')
genre_cols = genres.columns

my_ratings = my_ratings.merge(movies, on='movieId').merge(genres, left_on='movieId', right_index=True)

model = Lasso()
param_grid = {'alpha': sp_rand()}
rsearch = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=200, cv=20, random_state=42)

user1003 = my_ratings[my_ratings['userId'] == 1003]

rsearch.fit(user1003[genre_cols], user1003['rating'])

rsearch.best_estimator_.alpha

intercept = rsearch.best_estimator_.intercept_
coef = rsearch.best_estimator_.coef_

user1003_profile = pd.DataFrame([intercept, *coef], index=['intercept', *genre_cols], columns=['score'])

predictions = rsearch.best_estimator_.predict(genres)
genres['user1003'] = predictions

rating_predictions = genres[~genres.index.isin(user1003['movieId'])].sort_values('user1003', ascending=False)

rating_predictions = rating_predictions.merge(movies[['movieId', 'title']], left_index=True, right_on='movieId')

print(rating_predictions)
