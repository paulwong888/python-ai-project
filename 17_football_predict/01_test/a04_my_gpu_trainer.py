import time
import pandas as pd
import cupy as cp
import xgboost as xgb
from a01_2_my_dataset import MyDataset
# from a02_1_my_model import MyModel
# from a02_2_my_sgb_model import MyModel
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix, 
)

class MyGPUTrainer():
    def __init__(self, model):
        my_dataset = MyDataset()
        self.dataset = my_dataset.dataset
        self.le = my_dataset.le
        self.model = model
        self.params_gpu = {
            'tree_method': 'hist',
            'device': 'cuda',
        }

    def train(self):
        X_train, X_test, y_train, y_test = self.dataset
        
        print(len(X_train), len(y_train))
        print(len(X_test), len(y_test))

        X_train = cp.array(X_train)
        y_train = cp.array(y_train)
        X_test = cp.array(X_test)
        y_test = cp.array(y_test)

        # ---------------------------
        # 3. 训练模型
        # ---------------------------
        self.model.fit(X_train, y_train)

        # ---------------------------
        # 4. 评估模型
        # ---------------------------

        y_pred = self.model.predict(X_test)
        y_test = y_test.get()
        acc = accuracy_score(y_test, y_pred)
        print(f"准确率: {acc:.4f}")
        print(f"分类报告: {classification_report(y_test, y_pred, target_names=self.le.classes_)}")
        print(f"混淆矩阵: {confusion_matrix(y_test, y_pred)}")

    def predict_sgb(self):
        # ----------------------------
        # 5. 预测新比赛
        # ----------------------------
        # 示例：预测主队排名10 vs 客队排名30，主队近期胜率0.8，客队0.3，主场作战
        new_match = pd.DataFrame([{
            "home_rank": 10,
            "away_rank": 30,
            "home_form": 0.8,
            "away_form": 0.3,
            "is_home": 1
        }])
        new_match = cp.array(new_match)

        prediction = self.model.predict(new_match)
        print("\n预测结果:", self.le.inverse_transform(prediction)[0])

def test_sgb_boost():
    from a02_2_my_sgb_model import MyModel
    
    # model = MyModel().model
    model = MyModel().gpu_model
    print(model.get_params()["device"])

    my_trainer = MyGPUTrainer(model)
    my_trainer.train()
    my_trainer.predict_sgb()


if __name__ == "__main__":
    test_sgb_boost()