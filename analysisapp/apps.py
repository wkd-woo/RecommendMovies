from django.apps import AppConfig
from sklearn.linear_model import Lasso


class AnalysisappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysisapp'
    model = Lasso() # 장고 실행 시 모델을 app과 함께 한 번만 불러옴 : 속도 개선
