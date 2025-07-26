# Brute Force Time Estimator


![Python](https://img.shields.io/badge/python-3.8%2B-blue)

![License](https://img.shields.io/badge/license-MIT-green)

![GitHub stars](https://img.shields.io/github/stars/fx-xf/password-analyzer)

![GitHub issues](https://img.shields.io/github/issues/fx-xf/password-analyzer)Welcome to the **Password Strength Analyzer**, a Python-based tool that evaluates password strength using machine learning and generates secure passwords. This project leverages a custom linear regression model to predict password entropy and provides a user-friendly interface with rich text formatting.

## Features

- **Password Strength Analysis**: Evaluates password complexity based on features like length, character types, and entropy.
- **Secure Password Generation**: Generates random, secure passwords with customizable options (length, uppercase, digits, special characters).
- **Machine Learning Model**: Uses a custom linear regression model trained on the RockYou dataset to predict password entropy.
- **Interactive CLI**: Features a colorful, terminal-based interface using `rich` and `pyfiglet` for a polished user experience.
- **Data Visualization**: Generates plots to visualize password entropy data and model predictions.

## Project Structure

```
./
├── data/
│   ├── raw/
│   │   ├── rockyou.txt             # Raw password dataset
│   ├── processed/
│   │   ├── password_features.csv   # Processed password features
├── scripts/
│   ├── preprocessing/
│   │   ├── password_dataset_feature_engineering.py  # Feature extraction script
│   ├── training/
│   │   ├── train_password_model.py                 # Model training script
│   │   ├── models_linear_regression.py             # Custom linear regression implementation
├── main.py                    # Main application script
├── generate_password.py       # Password generation script
├── infer.py                  # Password strength inference script
├── password_time_model.pkl    # Trained model file
├── diagram.png               # Dataset visualization
├── diagram_predicted.png     # Model prediction visualization
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
├── .gitignore                # Git ignore file
├── .gitattributes            # Git attributes file
```

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/fx-xf/password-analyzer.git
   cd password-analyzer
   ```

2. **Create a Virtual Environment** (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the Dataset**:

   - Place the `rockyou.txt` dataset in `data/raw/`.
   - Run the preprocessing script to generate features:

     ```bash
     python scripts/preprocessing/password_dataset_feature_engineering.py
     ```

5. **Train the Model**:

   - Run the training script to generate `password_time_model.pkl`:

     ```bash
     python scripts/training/train_password_model.py
     ```

## Usage

Run the main application:

```bash
python main.py
```

### Menu Options

- **0: Check Password Strength** - Analyze a password's entropy and complexity using the trained model.
- **1: Generate Secure Password** - Create a random, secure password with customizable options.
- **2: About Developer** - View information about the developer.
- **3: Exit** - Close the application.

### Example

1. Select option `0` to check a password:

   ```
   Enter password to check: MyP@ssw0rd
   Password Analysis: MyP@ssw0rd
   Length: 10
   Digits: 1
   Lowercase letters: 6
   Uppercase letters: 2
   Special characters: 1
   Actual entropy: 59.46
   Complexity (actual): Medium
   Predicted entropy (model): 56.23
   Complexity (model): Medium
   ```

2. Select option `1` to generate a password:

   ```
   Enter password length (default 16): 12
   Use uppercase letters? (Y/n): Y
   Use digits? (Y/n): Y
   Use special characters? (Y/n): Y
   Your generated password: K7@mP#n9qL2x
   ```

## Dependencies

Listed in `requirements.txt`:

- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `tqdm`
- `rich`
- `pyfiglet`
- `colorama`

## Visualizations

- **diagram.png**: Scatter plot of the password dataset with training and test data.
- **diagram_predicted.png**: Comparison of actual and predicted entropy values.

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

Developed by fx-xf. For questions or feedback, open an issue or contact me via GitHub.

---

Enjoy securing your passwords with the Password Strength Analyzer!
