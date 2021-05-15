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

# load가 오래 걸려 우선은 inner data로 진행
ratings = pd.read_csv('analysisapp/data/ratings.csv')
genome_scores = pd.read_csv('analysisapp/data/genome-scores.csv')
genome_tags = pd.read_csv('analysisapp/data/genome-tags.csv')
my_ratings = pd.read_csv('analysisapp/data/my_ratings_input.csv')
movies = pd.read_csv('analysisapp/data/movies.csv')
with open('analysisapp/data/genres.p', 'rb') as f:
    genres = pickle.load(f)
genres = pd.read_pickle('analysisapp/data/genres.p')
genre_cols = genres.columns

genome_scores = pd.DataFrame[genome_scores.groupby('movieId')]
#genome_movies = movies.merge(movies, on='movieId').merge(genome_scores, left_on='movieId', right_index=True)
my_ratings = my_ratings.merge(movies, on='movieId').merge(genres, left_on='movieId', right_index=True)

#genome_movies = genome_movies[genome_movies.groupby('movieId')]
# ================ 환경 및 변수 설정 완료 ================

print(genome_scores)

class goRecommend():

    def guessYouLikeIt(self, userId):
        model = Lasso()  # 모델 설정
        param_grid = {'alpha': sp_rand()}
        rsearch = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=200, cv=20,
                                     random_state=42)

        YOU = my_ratings[my_ratings['userId'] == userId]  # 유저 설정, userID 값으로 YOU 설정

        rsearch.fit(YOU[genre_cols], YOU['rating'])  # 장르 칼럼

        rsearch.best_estimator_.alpha

        intercept = rsearch.best_estimator_.intercept_
        coef = rsearch.best_estimator_.coef_

        you_profile = pd.DataFrame([intercept, *coef],  # 유저 profile 생성. 장르별 계수
                                   index=['intercept', *genre_cols], columns=['score'])

        predictions = rsearch.best_estimator_.predict(genres)
        genres['YOU'] = predictions

        rating_predictions = genres[~genres.index.isin(YOU['movieId'])].sort_values('YOU', ascending=False)
        rating_predictions = rating_predictions.merge(movies[['movieId', 'title']], left_index=True, right_on='movieId')

        Top5 = rating_predictions.sort_values(by='YOU', ascending=False)[:5] # 추천 TOP 5
        Worst5 = rating_predictions.sort_values(by='YOU', ascending=True)[:5] # 비추천 WORST 5
        print(Top5)  # 예상 별점! 이를 토대로 can show best , worst or whatever something


class YourProfile():

    def showRateDistribution(self):
        YOU = my_ratings[my_ratings['userId'] == 1003]  # 유저 설정
        YourDistribution = YOU['rating'].hist()  # 평점 분포 히스토그램 : 프론트에서 graph를 보여주려면? -> 찾아보기. 이후 profile 적용 !
