#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import pickle
import numpy as np
import pandas as pd
import string

# Add training directory to path for model import
script_dir = os.path.dirname(os.path.abspath(__file__))
training_dir = os.path.join(script_dir, 'scripts', 'training')
sys.path.append(training_dir)

try:
    from models_linear_regression import MyLinearRegression
except ImportError as e:
    print(f"Error importing model: {e}")
    sys.exit(1)

def extract_features(password):
    """Extracts features from a password for model prediction."""
    features = {}
    features['length'] = len(password)
    
    features['num_digits'] = sum(1 for char in password if char.isdigit())
    features['num_lower'] = sum(1 for char in password if char.islower())
    features['num_upper'] = sum(1 for char in password if char.isupper())
    features['num_special'] = sum(1 for char in password if char in string.punctuation or not char.isalnum())
    
    features['has_digit'] = int(features['num_digits'] > 0)
    features['has_lower'] = int(features['num_lower'] > 0)
    features['has_upper'] = int(features['num_upper'] > 0)
    features['has_special'] = int(features['num_special'] > 0)
    
    charset_size = 0
    if features['has_digit']: charset_size += 10  
    if features['has_lower']: charset_size += 26  
    if features['has_upper']: charset_size += 26  
    if features['has_special']: charset_size += 32  
    
    features['entropy'] = features['length'] * np.log2(charset_size) if charset_size > 0 else 0
    
    return features

def load_model(model_path):
    """Loads the trained model from a pickle file."""
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        print(f"Error: Model not found at path {model_path}.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

def main():
    """Main function to analyze password strength using the trained model."""
    if len(sys.argv) != 2:
        print("Usage: python infer.py <path_to_model.pkl>")
        sys.exit(1)

    model_path = sys.argv[1]
    
    if not os.path.exists(model_path):
        print(f"Model not found at path: {model_path}")
        sys.exit(1)
    
    model = load_model(model_path)
    
    try:
        password = input("Enter password to check: ")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except EOFError:
        print("\nInput error.")
        sys.exit(1)
    
    if not password:
        print("Password cannot be empty.")
        sys.exit(1)

    features = extract_features(password)
    
    df_features = pd.DataFrame([features])
    
    # Use only the 'length' feature for prediction as per training
    X_input = df_features[['length']].values.astype(np.float64)
    
    try:
        predicted_entropy = model.predict(X_input)[0]
    except Exception as e:
        print(f"Error during model prediction: {e}")
        sys.exit(1)
    
    actual_entropy = features['entropy']
    
    # Categorize actual entropy
    if actual_entropy <= 0:
        actual_strength = "Very Weak (no characters)"
    elif actual_entropy < 25:
        actual_strength = "Very Weak"
    elif actual_entropy < 45:
        actual_strength = "Weak"
    elif actual_entropy < 65:
        actual_strength = "Medium"
    elif actual_entropy < 85:
        actual_strength = "Good"
    else:
        actual_strength = "Excellent"
        
    # Categorize predicted entropy
    if predicted_entropy <= 0:
        pred_strength = "Very Weak (by model)"
    elif predicted_entropy < 25:
        pred_strength = "Very Weak (by model)"
    elif predicted_entropy < 45:
        pred_strength = "Weak (by model)"
    elif predicted_entropy < 65:
        pred_strength = "Medium (by model)"
    elif predicted_entropy < 85:
        pred_strength = "Good (by model)"
    else:
        pred_strength = "Excellent (by model)"

    result_text = f"""
Password Analysis: {password}

Length: {features['length']}
Digits: {features['num_digits']}
Lowercase letters: {features['num_lower']}
Uppercase letters: {features['num_upper']}
Special characters: {features['num_special']}

Actual entropy: {actual_entropy:.2f}
Complexity (actual): {actual_strength}

Predicted entropy (model): {predicted_entropy:.2f}
Complexity (model): {pred_strength}
"""
    print(result_text)

if __name__ == "__main__":
    main()