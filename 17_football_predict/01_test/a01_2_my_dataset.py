import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ----------------------------
# 1. 模拟数据生成（假设没有真实数据）
# ----------------------------
# 特征示例：主队排名、客队排名、主队近5场胜率、客队近5场胜率、场地类型（0=中立，1=主场）
class MyDataset():
    def __init__(self):
        self.le = LabelEncoder()
        origin_dataset = self.build_origin_dataset()
        X, y = self.build_features(origin_dataset)
        X_train, X_test, y_train, y_test = self.train_test_split(X, y)
        self.dataset = X_train, X_test, y_train, y_test


    def build_origin_dataset(self):
        # ----------------------------
        # 1. 模拟数据生成（假设没有真实数据）
        # ----------------------------
        # 特征示例：主队排名、客队排名、主队近5场胜率、客队近5场胜率、场地类型（0=中立，1=主场）
        np.random.seed(42)
        num_matches = 100000
        data = {
            "home_rank": np.random.randint(1, 50, num_matches),
            "away_rank": np.random.randint(1, 50, num_matches),
            "home_form": np.random.uniform(0, 1, num_matches),
            "away_form": np.random.uniform(0, 1, num_matches),
            "is_home": np.random.choice([0, 1], num_matches),
        }
        df = pd.DataFrame(data)

        return df
    
    def build_features(self, df: DataFrame):

        # 根据特征生成标签（假设主队排名越高、近期胜率越高，胜率越大）
        # 这里简化逻辑：主队优势 = (home_form - away_form) + (away_rank - home_rank)/100
        df["result"] = np.where(
            df["home_form"] - df["away_form"] + (df["away_rank"] - df["home_rank"])/100 > 0.1,
            "home_win",
            np.where(
                abs(df["home_form"] - df["away_form"]) < 0.05,
                "draw",
                "away_win"
            )
        )
        
        # ----------------------------
        # 2. 数据预处理
        # ----------------------------
        # 编码标签（将文本标签转为数字）
        # lb = LabelEncoder()
        df["result_encoded"] = self.le.fit_transform(df["result"])

        # 选择特征列
        features = ["home_rank", "away_rank", "home_form", "away_form", "is_home"]

        X = df[features]
        y = df["result_encoded"]

        return X, y
    
    def train_test_split(self, X: DataFrame, y: DataFrame):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    
if __name__ == "__main__":
    my_dataset = MyDataset()
    print(my_dataset.dataset)