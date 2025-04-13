import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split

# ----------------------------
# 1. 模拟数据生成（假设没有真实数据）
# ----------------------------
# 特征示例：主队排名、客队排名、主队近5场胜率、客队近5场胜率、场地类型（0=中立，1=主场）
class MyDataset():
    def __init__(self):
        origin_dataset = self.build_origin_dataset()
        X, y = self.build_features(origin_dataset)
        X_train, X_test, y_train, y_test = self.train_test_split(X, y)
        self.dataset = X_train, X_test, y_train, y_test


    def build_origin_dataset(self):
        # ---------------------------
        # 1. 模拟历史比赛数据（实际需替换为真实数据）
        # ---------------------------
        # 特征示例：主队场均进球、客队场均失球、主队世界排名、客队世界排名、场地类型（0=中立,1=主场）
        # 标签：比赛结果（0=客胜, 1=平局, 2=主胜）
        np.random.seed(42)
        num_matches = 100000
        data = {
            "home_avg_goals": np.random.normal(1.5, 0.5, num_matches),
            "away_avg_goals": np.random.normal(1.3, 0.4, num_matches),
            "home_rank": np.random.normal(1, 100, num_matches),
            "away_rank": np.random.normal(1, 100, num_matches),
            "is_home": np.random.choice([0, 1], num_matches),
            "result": np.random.choice([0, 1, 2], num_matches),
        }

        df = pd.DataFrame(data)

        return df
    
    def build_features(self, df: DataFrame):

        # ---------------------------
        # 2. 特征工程
        # ---------------------------
        # 添加自定义特征：排名差、攻防差值
        df["rank_diff"] = df["away_rank"] - df["home_rank"]
        df["attack_defense_ratio"] = df["home_avg_goals"] / df["away_avg_goals"]

        # 选择特征列
        features = ["home_avg_goals", "away_avg_goals", "rank_diff", "attack_defense_ratio", "is_home"]

        X = df[features]
        y = df["result"]

        return X, y
    
    def train_test_split(self, X: DataFrame, y: DataFrame):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    
if __name__ == "__main__":
    my_dataset = MyDataset()
    print(my_dataset.dataset)