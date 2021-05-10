import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Lasso
import pickle
import os
import warnings

currentpath = os.getcwd()
warnings.filterwarnings('ignore')

rating_path = 'analysisapp/data/ratings.csv'
my_rating_path = 'analysisapp/data/my_ratings_input.csv'
movie_path = 'analysisapp/data/movies.csv'
genre_path = 'analysisapp/data/genres.p'

ratings = pd.read_csv(rating_path)
my_ratings = pd.read_csv(my_rating_path)
movies = pd.read_csv(movie_path)
genres = pd.read_pickle(genre_path)

my_ratings.shape

my_ratings = my_ratings.merge(movies, on='movieId').merge(genres, left_on='movieId', right_index=True)

my_ratings.shape
my_ratings.sample()

"""## user1002"""

user1002 = my_ratings[my_ratings['userId'] == 1002]

user1002.shape

user1002['rating'].hist()

user1002['rating'].value_counts()

user1002['rating'].describe()

user1002[user1002['rating']==2.0]

genre_cols = genres.columns

user1002[genre_cols].sum().sort_values(ascending=False)

"""## 나와 친구의 취향 차이"""

my_ratings['movieId'].value_counts().sort_values(ascending=False)

my_ratings[my_ratings['movieId'] == 97938]

"""호불호가 가장 심한 장르를 찾아보자
 - 같이 영화를 보려면 반드시 피해야 하는 장르
"""

my_ratings_v1 = my_ratings.copy()
my_ratings_v1 = my_ratings_v1.replace(0, np.nan)

for col in genre_cols:
  my_ratings_v1[col] = my_ratings_v1[col] * my_ratings_v1['rating']

user_profile_v1 = my_ratings_v1.groupby('userId')[genre_cols].mean()
user_profile_v1

user_profile_describe = user_profile_v1.describe()
user_profile_describe

user_profile_describe.loc[:, user_profile_describe.loc['count'] == 2]

thriller = my_ratings[my_ratings['Thriller'] == 1]

sns.boxplot(data=thriller, x='userId', y='rating')

"""## Lasso로 user profile 만들기"""

model = Lasso()
model
# alpha : 정규화 텀 (계수의 크기를 조절하는 것)

"""### 하이퍼 파라미터 튜닝

"""

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform as sp_rand

param_grid = {'alpha': sp_rand()}

rsearch = RandomizedSearchCV(estimator=model, param_distributions=param_grid, n_iter=200, cv=20, random_state=42)

user1001 = my_ratings[my_ratings['userId'] == 1001]
user1002 = my_ratings[my_ratings['userId'] == 1002]
user1003 = my_ratings[my_ratings['userId'] == 1003]

rsearch.fit(user1003[genre_cols], user1003['rating'])

rsearch.best_estimator_.alpha

intercept = rsearch.best_estimator_.intercept_
coef = rsearch.best_estimator_.coef_

user1003_profile = pd.DataFrame([intercept, *coef], index=['intercept', *genre_cols], columns=['score'])
user1003_profile

plt.figure(figsize=(25, 7))
sns.barplot(data=user1003_profile.reset_index(), x='index', y='score')

predictions = rsearch.best_estimator_.predict(genres)
predictions

genres['user1003'] = predictions

rating_predictions = genres[~genres.index.isin(user1003['movieId'])].sort_values('user1003', ascending=False)
rating_predictions.head()

rating_predictions = rating_predictions.merge(movies[['movieId', 'title']], left_index=True, right_on='movieId')
rating_predictions

