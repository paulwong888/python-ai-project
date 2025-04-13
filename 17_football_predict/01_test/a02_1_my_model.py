from sklearn.ensemble import RandomForestClassifier

class MyModel():
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100, 
            # max_depth=300,
            random_state=42,
        )