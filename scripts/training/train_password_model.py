from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from models_linear_regression import MyLinearRegression

def linear_expression(x):
    """Defines a linear function for plotting the ideal relationship."""
    return 5 * x + 6

def main():
    """Trains a linear regression model on password features and saves it."""
    try:
        # Load and clean data
        df = pd.read_csv('data/processed/password_features.csv')
        df_clean = df.replace([np.inf, -np.inf], np.nan).dropna()
        
        # Prepare features and target
        X = df_clean.drop(columns=['password', 'entropy'])
        y = df_clean['entropy']
        
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Limit points for plotting
        max_points = 1000
        
        # Prepare training data for plotting
        train_size = min(len(X_train), len(y_train), max_points)
        if len(X_train) > max_points:
            indices = np.random.choice(len(X_train), train_size, replace=False)
            X_train_plot = X_train.iloc[indices, 0]
            y_train_plot = y_train.iloc[indices]
        else:
            X_train_plot = X_train.iloc[:, 0]
            y_train_plot = y_train
        
        # Prepare test data for plotting
        test_size = min(len(X_test), len(y_test), max_points)
        if len(X_test) > max_points:
            indices = np.random.choice(len(X_test), test_size, replace=False)
            X_test_plot = X_test.iloc[indices, 0]
            y_test_plot = y_test.iloc[indices]
        else:
            X_test_plot = X_test.iloc[:, 0]
            y_test_plot = y_test
        
        # Plot dataset
        plt.figure(figsize=(10, 6))
        X_line = X.iloc[:, 0]
        plt.plot(X_line, linear_expression(X_line), label='real', c='g')
        plt.scatter(X_train_plot, y_train_plot, label='train', c='b', alpha=0.6)
        plt.scatter(X_test_plot, y_test_plot, label='test', c='orange', alpha=0.6)
        plt.title("Password Entropy Dataset")
        plt.xlabel("Feature values")
        plt.ylabel("Entropy")
        plt.grid(alpha=0.2)
        plt.legend()
        plt.savefig('diagram.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Train model using only the 'length' feature
        X_train_np = X_train.iloc[:, 0].values
        X_test_np = X_test.iloc[:, 0].values
        X_train_2d = X_train_np.reshape(-1, 1).astype(np.float64)
        X_test_2d = X_test_np.reshape(-1, 1).astype(np.float64)
        y_train = y_train.astype(np.float64)
        y_test = y_test.astype(np.float64)
        
        regressor = MyLinearRegression()
        regressor.fit(X_train_2d, y_train)
        predictions = regressor.predict(X_test_2d)
        
        # Print model weights
        w = regressor.get_weights()
        print("Model weights:", w)
        
        # Plot predictions
        plt.figure(figsize=(10, 18))
        X_for_plot = X.iloc[:, 0].values.reshape(-1, 1)
        y_pred_all = regressor.predict(X_for_plot)
        
        ax = None
        for i, types in enumerate([['train', 'test'], ['train'], ['test']]):
            ax = plt.subplot(3, 1, i + 1, sharey=ax)
            if 'train' in types:
                plt.scatter(X_train_plot, y_train_plot, label='train', c='b')
            if 'test' in types:
                plt.scatter(X_test_plot, y_test_plot, label='test', c='orange')
            plt.plot(X_line, linear_expression(X_line), label='real', c='g')
            plt.plot(X_line, y_pred_all, label='predicted', c='r')
            plt.ylabel('target')
            plt.xlabel('feature')
            plt.title(" ".join(types))
            plt.grid(alpha=0.2)
            plt.legend()

        plt.savefig('diagram_predicted.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save the trained model
        model_filename = 'password_time_model.pkl'
        with open(model_filename, 'wb') as f:
            pickle.dump(regressor, f)
        print(f"Model successfully saved to '{model_filename}'")

    except Exception as e:
        print(f"Error in main code: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()