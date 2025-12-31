class ClassificationModels:
    def train(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def evaluate(self, y_true, y_pred):
        raise NotImplementedError
