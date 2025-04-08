import pandas as pd
from a01_2_my_dataset import MyDataset
# from a02_1_my_model import MyModel
# from a02_2_my_sgb_model import MyModel
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class MyTrainer():
    def __init__(self, model):
        my_dataset = MyDataset()
        self.dataset = my_dataset.dataset
        self.le = my_dataset.le
        self.model = model

    def train(self):
        X_train, X_test, y_train, y_test = self.dataset
        print(len(X_train), len(y_train))
        print(len(X_test), len(y_test))

        # ---------------------------
        # 3. 训练模型
        # ---------------------------
        self.model.fit(X_train, y_train)

        # ---------------------------
        # 4. 评估模型
        # ---------------------------
        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"准确率: {acc:.4f}")
        print(f"分类报告: {classification_report(y_test, y_pred, target_names=self.le.classes_)}")
        print(f"混淆矩阵: {confusion_matrix(y_test, y_pred)}")


    def predict_random_forest(self):
        # ---------------------------
        # 5. 单场比赛预测示例
        # ---------------------------
        # 示例输入：主队场均进球1.8，客队场均失球1.2，主队排名30，客队排名50，主场作战
        new_match = [[1.8, 1.2, 50-30, 1.8/1.2, 1]]
        prediction = self.model.predict(new_match)
        print(f"Predicted result: {['Away Win', 'Draw', 'Home Win'][prediction[0]]}")

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

        prediction = self.model.predict(new_match)
        print("\n预测结果:", self.le.inverse_transform(prediction)[0])

def test_random_forest():
    from a02_1_my_model import MyModel
    
    my_trainer = MyTrainer(MyModel().model)
    my_trainer.train()

    my_trainer.predict_random_forest()

def test_sgb_boost():
    from a02_2_my_sgb_model import MyModel
    
    my_trainer = MyTrainer(MyModel().model)
    my_trainer.train()
    my_trainer.predict_sgb()


if __name__ == "__main__":
    test_random_forest()
    test_sgb_boost()