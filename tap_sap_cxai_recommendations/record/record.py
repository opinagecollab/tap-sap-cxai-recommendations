from enum import Enum


class Record(Enum):
    SCORES = 'product_scores'
    RECOMMENDATIONS = 'recommendations'
    RECOMMENDATION_MODELS = 'recommendation_models'
    RECOMMENDATION_SUBSTITUTIONS = 'recommendation_substitutions'
    USERS = 'users'
    PAGE_TYPES = 'page_types'
    PAGETYPE_MODEL = 'pagetype_model'
