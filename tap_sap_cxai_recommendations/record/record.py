from enum import Enum


class Record(Enum):
    SCORES = 'product_scores'
    RECOMMENDATIONS = 'recommendations'
    RECOMMENDATION_MODELS = 'recommendation_models'
    USERS = 'users'
