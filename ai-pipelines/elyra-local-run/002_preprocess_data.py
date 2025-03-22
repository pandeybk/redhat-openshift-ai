import os
import pandas as pd
import numpy as np
import argparse
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib

def load_dataset(file_path):
    df = pd.read_csv(file_path)
    print(f"Dataset loaded successfully from {file_path}")
    return df

def handle_missing_values(df):
    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')

    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())

    print("Missing values handled.")
    return df

def select_features(df):
    selected_columns = [
        'proto', 'service', 'state', 'sbytes', 'dbytes', 'sttl', 'dttl',
        'sloss', 'dloss', 'sload', 'dload', 'spkts', 'dpkts', 'attack_cat', 'label'
    ]
    df = df[selected_columns]
    print("Features selected.")
    return df

def encode_features(df):
    """
    Encodes categorical variables and scales numerical features.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        np.ndarray: Transformed feature array.
        np.ndarray: Label array.
        ColumnTransformer: Fitted transformer for future use.
    """
    # Separate features and labels
    X = df.drop(['label', 'attack_cat'], axis=1)
    y = df['label']

    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Define transformers
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse=False)
    numerical_transformer = StandardScaler()

    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_cols),
            ('num', numerical_transformer, numerical_cols)
        ])

    # Fit and transform the data
    X_transformed = preprocessor.fit_transform(X)

    print("Features encoded and scaled.")
    return X_transformed, y.values, preprocessor

def save_processed_data(X_train, X_test, y_train, y_test, preprocessor, output_dir):
    """
    Saves the processed data and preprocessor for future use.

    Args:
        X_train, X_test, y_train, y_test: Training and testing data.
        preprocessor (ColumnTransformer): Fitted preprocessor.
        output_dir (str): Directory to save processed data.
    """
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(X_train, os.path.join(output_dir, 'X_train.pkl'))
    joblib.dump(X_test, os.path.join(output_dir, 'X_test.pkl'))
    joblib.dump(y_train, os.path.join(output_dir, 'y_train.pkl'))
    joblib.dump(y_test, os.path.join(output_dir, 'y_test.pkl'))
    joblib.dump(preprocessor, os.path.join(output_dir, 'preprocessor.pkl'))

    print(f"Processed data saved to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Preprocess Raw Dataset")
    parser.add_argument('--file_path', type=str, default='./data/raw/UNSW_NB15_training-set.csv', help='Path to the raw dataset CSV file (default: "./data/raw/UNSW_NB15_training-set.csv")')
    parser.add_argument('--output_dir', type=str, default='./data/processed', help='Directory to save processed data (default: "./data/processed")')
    
    args = parser.parse_args()

    # Load, preprocess, and save data
    df = load_dataset(args.file_path)
    df = handle_missing_values(df)
    df = select_features(df)
    X, y, preprocessor = encode_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Data split into training and testing sets.")
    save_processed_data(X_train, X_test, y_train, y_test, preprocessor, args.output_dir)

if __name__ == "__main__":
    main()
