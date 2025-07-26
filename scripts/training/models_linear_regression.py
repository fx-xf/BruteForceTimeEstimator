import numpy as np

class MyLinearRegression:
    def __init__(self):
        self.w = None

    def fit(self, X, y):
        # Принимаем на вход X, y и вычисляем веса по данной выборке
        # Не забываем про фиктивный признак равный 1
        X = np.array(X)
        y = np.array(y)
        assert len(y.shape) == 1 and len(X.shape) == 2
        assert X.shape[0] == y.shape[0]

        y = y[:, np.newaxis] # делаем размерность ell, 1
        l, n = X.shape[0], X.shape[1]

        # Исправленная строка: правильно создаем массив единиц
        X_train = np.hstack((X, np.ones((l, 1))))
        
        # Используем solve вместо inv для лучшей численной стабильности
        A = X_train.T @ X_train
        b = X_train.T @ y
        self.w = np.linalg.solve(A, b)  # Вместо np.linalg.inv(A) @ b

        return self
    
    def predict(self, X):
        # Принимает на вход X и возвращает ответы модели
        # Не забываем про фиктивный признак равный 1
        X = np.array(X)
        l = X.shape[0]

        # Исправленная строка: правильно добавляем столбец единиц
        X_train = np.hstack((X, np.ones((l, 1))))

        y_pred = X_train @ self.w

        return y_pred.flatten()  # Возвращаем одномерный массив
    
    def get_weights(self):
        return self.w.copy().flatten()  # Возвращаем одномерный массив весов