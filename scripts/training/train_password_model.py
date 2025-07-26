from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gc
import pickle 
from models_linear_regression import MyLinearRegression

def linear_expression(x):
    return 5 * x + 6

try:
    df = pd.read_csv('data/processed/password_features.csv')
    df_clean = df.replace([np.inf, -np.inf], np.nan).dropna()
    
    X = df_clean.drop(columns=['password', 'entropy'])
    y = df_clean['entropy']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Ограничение точек для графика
    max_points = 1000
    
    # Подготовка данных для train
    train_size = min(len(X_train), len(y_train), max_points)
    if len(X_train) > max_points:
        indices = np.random.choice(len(X_train), train_size, replace=False)
        X_train_plot = X_train.iloc[indices, 0] if len(X_train.shape) > 1 else X_train.iloc[indices]
        y_train_plot = y_train.iloc[indices]
    else:
        X_train_plot = X_train.iloc[:, 0] if len(X_train.shape) > 1 else X_train
        y_train_plot = y_train
    
    # Подготовка данных для test
    test_size = min(len(X_test), len(y_test), max_points)
    if len(X_test) > max_points:
        indices = np.random.choice(len(X_test), test_size, replace=False)
        X_test_plot = X_test.iloc[indices, 0] if len(X_test.shape) > 1 else X_test.iloc[indices]
        y_test_plot = y_test.iloc[indices]
    else:
        X_test_plot = X_test.iloc[:, 0] if len(X_test.shape) > 1 else X_test
        y_test_plot = y_test
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    
    # Линия
    X_line = X.iloc[:, 0] if len(X.shape) > 1 else X
    plt.plot(X_line, linear_expression(X_line), label='real', c='g')
    
    # Точки
    plt.scatter(X_train_plot, y_train_plot, label='train', c='b', alpha=0.6)
    plt.scatter(X_test_plot, y_test_plot, label='test', c='orange', alpha=0.6)
    
    plt.title("Password Entropy Dataset")
    plt.xlabel("Feature values")
    plt.ylabel("Entropy")
    plt.grid(alpha=0.2)
    plt.legend()
    plt.savefig('diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Обучение модели
    # Преобразование данных для обучения
    X_train_np = X_train.iloc[:, 0].values if len(X_train.shape) > 1 else X_train.values
    X_test_np = X_test.iloc[:, 0].values if len(X_test.shape) > 1 else X_test.values
    
    # Преобразование в нужный формат
    X_train_2d = X_train_np.reshape(-1, 1)
    X_test_2d = X_test_np.reshape(-1, 1)
    
    # Преобразование в float для избежания ошибок типов
    X_train_2d = X_train_2d.astype(np.float64)
    y_train = y_train.astype(np.float64)
    X_test_2d = X_test_2d.astype(np.float64)
    y_test = y_test.astype(np.float64)
    
    regressor = MyLinearRegression()
    regressor.fit(X_train_2d, y_train)
    predictions = regressor.predict(X_test_2d)
    
    # Вывод весов
    w = regressor.get_weights()
    print("Веса модели:", w)
    
    # Построение графиков предсказаний
    plt.figure(figsize=(10, 18))

    # Подготовка данных для графика предсказаний
    X_for_plot = X.iloc[:, 0].values.reshape(-1, 1) if len(X.shape) > 1 else X.values.reshape(-1, 1)
    y_pred_all = regressor.predict(X_for_plot)
    
    ax = None

    for i, types in enumerate([['train', 'test'], ['train'], ['test']]):
        ax = plt.subplot(3, 1, i + 1, sharey=ax)
        if 'train' in types:
            plt.scatter(X_train_plot, y_train_plot, label='train', c='b')
        if 'test' in types:
            plt.scatter(X_test_plot, y_test_plot, label='test', c='orange')

        # Используем подготовленные данные
        X_line_plot = X.iloc[:, 0] if len(X.shape) > 1 else X
        plt.plot(X_line_plot, linear_expression(X_line_plot), label='real', c='g')
        plt.plot(X_line_plot, y_pred_all, label='predicted', c='r')

        plt.ylabel('target')
        plt.xlabel('feature')
        plt.title(" ".join(types))
        plt.grid(alpha=0.2)
        plt.legend()

    plt.savefig('diagram_predicted.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    model_filename = 'password_time_model.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(regressor, f)
    print(f"Модель успешно сохранена в файл '{model_filename}'")

    gc.collect()

except Exception as e:
    print(f"Ошибка в основном коде: {e}")
    import traceback
    traceback.print_exc()