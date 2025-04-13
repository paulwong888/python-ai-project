from xgboost import XGBClassifier

class MyModel():
    def __init__(self):
        self.model = XGBClassifier(
            objective = 'multi:softmax',  # 多分类任务
            num_class = 3,                # 3种结果：home_win/draw/away_win
            n_estimators = 100,
            learning_rate = 0.1,
        )
        self.gpu_model = XGBClassifier(
            objective = 'multi:softmax',  # 多分类任务
            num_class = 3,                # 3种结果：home_win/draw/away_win
            n_estimators = 100,
            learning_rate = 0.1,
            tree_method = "hist",
            device = "cuda",
        )