import os
import pickle
import warnings
import pandas as pd
import numpy as np
from scipy.stats import uniform as sp_rand
from sklearn.model_selection import RandomizedSearchCV
from .apps import AnalysisappConfig
from .models import Results

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
my_ratings = pd.read_csv('analysisapp/data/my_ratings_input.csv')
movies = pd.read_csv('analysisapp/data/movies.csv')
with open('analysisapp/data/genres.p', 'rb') as f:
    genres = pickle.load(f)
genres = pd.read_pickle('analysisapp/data/genres.p')
genre_cols = genres.columns

genre_dict = {1: 'Action', 2: 'Adventure', 3: 'Animation', 4: 'Children', 5: 'Comedy', 6: 'Crime', 7: 'Documentary',
              8: 'Drama', 9: 'Fantasy', 10: 'Film-Noir', 11: 'Horror', 12: 'IMAX', 13: 'Musical', 14: 'Mystery',
              15: 'Romance', 16: 'Sci-Fi', 17: 'Thriller', 18: 'War', 19: 'Western'}

my_ratings = my_ratings.merge(movies, on='movieId').merge(genres, left_on='movieId', right_index=True)


# ================ 환경 및 변수 설정 완료 ================ #


class goRecommend():
    def Predict(self, userId):
        param_grid = {'alpha': sp_rand()}
        rsearch = RandomizedSearchCV(estimator=AnalysisappConfig.model, param_distributions=param_grid, n_iter=200,
                                     cv=20,
                                     random_state=42)  # model: Lasso

        YOU = my_ratings[my_ratings['userId'] == userId]  # 유저 설정, userID 값으로 YOU 설정

        rsearch.fit(YOU[genre_cols], YOU['rating'])  # 장르 칼럼

        #rsearch.best_estimator_.alpha

        intercept = rsearch.best_estimator_.intercept_
        coef = rsearch.best_estimator_.coef_

        """
        you_profile = pd.DataFrame([intercept, *coef],  # 유저 profile 생성. 장르별 계수
                                   index=['intercept', *genre_cols], columns=['score'])
        """
        predictions = rsearch.best_estimator_.predict(genres)
        genres['YOU'] = predictions

        rating_predictions = genres[~genres.index.isin(YOU['movieId'])].sort_values('YOU', ascending=False)
        rating_predictions = rating_predictions.merge(movies[['movieId', 'title']], left_index=True, right_on='movieId')

        return rating_predictions  # 예상 별점! it can show the best, worst or whatever something


class YourProfile():
    def showRateDistribution(self):
        YOU = my_ratings[my_ratings['userId'] == 1003]  # 유저 설정
        YourDistribution = YOU['rating'].hist()  # 평점 분포 히스토그램 : 프론트에서 graph를 보여주려면? -> 찾아보기. 이후 profile 적용 !
        return




def guessYouLikeIt(rating_predictions, userId):
    Top12 = rating_predictions.sort_values(by='YOU', ascending=False)[:12]  # 추천 TOP 12

    Top12 = list(Top12[['movieId', 'YOU']].to_dict().values())
    Top12 = dict(zip(list(Top12[0].values()), list(Top12[1].values())))
    return Top12  # ItCanBeYourTop12

def guessYouHateIt(rating_predictions, userId):
    Worst12 = rating_predictions.sort_values(by='YOU', ascending=True)[:12]  # 비추천 TOP 12

    Worst12 = list(Worst12[['movieId', 'YOU']].to_dict().values())
    Worst12 = dict(zip(list(Worst12[0].values()), list(Worst12[1].values())))
    return Worst12  # ItCanBeYourWorst12

def genreThatYouLike(rating_predictions, userId, genre):
    GenreTop12 = rating_predictions[rating_predictions[genre_dict[genre]]
                                    != 0].sort_values(by='YOU', ascending=False)[:12]  # 장르 추천 TOP 12
    GenreTop12 = list(GenreTop12[['movieId', 'YOU']].to_dict().values())
    GenreTop12 = dict(zip(list(GenreTop12[0].values()), list(GenreTop12[1].values())))
    return GenreTop12  # 장르 Top 12
