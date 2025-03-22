# n03_train_model_component.py

import kfp
from kfp import dsl
from kfp.dsl import component, InputPath, OutputPath

@component(
    packages_to_install=['scikit-learn', 'joblib', 'pandas'],
)
def train_model_component(
    processed_data_path: InputPath(),
    model_output_path: OutputPath(),
):
    import os
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd
    import numpy as np

    # Load preprocessed data
    X = pd.read_pickle(os.path.join(processed_data_path, 'X.pkl'))
    y_encoded = joblib.load(os.path.join(processed_data_path, 'y_encoded.pkl'))

    # Convert X to NumPy array
    X_values = X.values.astype(np.float32)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_values, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    print("Train-test split completed.")

    # Model training using RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("RandomForestClassifier model training completed.")

    # Save model and test data
    os.makedirs(model_output_path, exist_ok=True)
    joblib.dump(model, os.path.join(model_output_path, 'model.joblib'))
    joblib.dump(X_test, os.path.join(model_output_path, 'X_test.pkl'))
    joblib.dump(y_test, os.path.join(model_output_path, 'y_test.pkl'))
    print(f"Model and test data saved to {model_output_path}")
