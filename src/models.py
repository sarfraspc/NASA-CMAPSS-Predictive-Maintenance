import joblib

def load_model(path):
    return joblib.load(path)

def predict_rul(model, X):
    return model.predict(X)
