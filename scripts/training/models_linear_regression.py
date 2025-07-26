import numpy as np

class MyLinearRegression:
    """Custom linear regression implementation for password entropy prediction."""

    def __init__(self):
        self.w = None  # Model weights

    def fit(self, X, y):
        """Trains the model using the normal equation method."""
        X = np.array(X)
        y = np.array(y)
        assert len(y.shape) == 1 and len(X.shape) == 2
        assert X.shape[0] == y.shape[0]

        y = y[:, np.newaxis]  # Reshape y to (n, 1)
        l, n = X.shape[0], X.shape[1]

        # Add bias term (column of ones)
        X_train = np.hstack((X, np.ones((l, 1))))
        
        # Compute weights using normal equation
        A = X_train.T @ X_train
        b = X_train.T @ y
        self.w = np.linalg.solve(A, b)  # Solve for weights

        return self
    
    def predict(self, X):
        """Predicts entropy values for input features."""
        X = np.array(X)
        l = X.shape[0]

        # Add bias term
        X_train = np.hstack((X, np.ones((l, 1))))

        y_pred = X_train @ self.w
        return y_pred.flatten()  # Return 1D array
    
    def get_weights(self):
        """Returns the model weights."""
        return self.w.copy().flatten()  # Return 1D array of weights