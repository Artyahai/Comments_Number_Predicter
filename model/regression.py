import numpy as np
import psycopg2
import pandas as pd 
class MultiLinearregression:
    def __init__(self, lr=0.01, epochs = 10000):
        self.lr = lr
        self.epochs = epochs
        self.w = None 
        self.b = None 
        self.loss_history = []
    def fit(self,X,y):
        n, m = X.shape
        self.w = np.zeros(m)
        self.b = 0.0
        for epoch in range(self.epochs):
            y_pred = X.dot(self.w) + self.b 
            loss = np.mean((y - y_pred) ** 2)
            self.loss_history.append(loss)
            dw = (-2/n) * (X.T.dot(y - y_pred))
            db = (-2/n) * np.sum(y - y_pred)
            self.w -=self.lr * dw
            self.b -= self.lr * db
            if epoch % 1000 == 0:
                print(f"epoch: {epoch}, loss: {loss:.4f}")
    def predict(self,X):
        return X.dot(self.w) + self.b 

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) **2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

def train_test_split(X, y, test_size = 0.2):
    incides = np.arange(len(X))
    np.random.shuffle(incides)
    test_count = int(len(X) * test_size)
    test_idx = incides[:test_count]
    train_idx = incides[test_count:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

def standartize(X_train, X_test):
    mean = X_train.mean(axis = 0)
    std = X_train.std(axis = 0)
    X_train_scaled  = (X_train - mean) / std
    X_test_scaled = (X_test - mean)/std
    return X_train_scaled, X_test_scaled


conn = psycopg2.connect("host='localhost' port=5432 dbname='dataset' user='postgres' password='postgres'")
query = """ 
SELECT likes, repostscount, commentcount, views FROM Xinfo; """
df = pd.read_sql(query, conn)
print(df)

    