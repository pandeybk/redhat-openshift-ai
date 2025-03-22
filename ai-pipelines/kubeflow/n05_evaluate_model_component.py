# n05_evaluate_model_component.py

import kfp
from kfp import dsl
from kfp.dsl import component, InputPath

@component(
    packages_to_install=['scikit-learn', 'joblib', 'pandas', 'matplotlib', 'seaborn'],
)
def evaluate_model_component(
    model_input_path: InputPath(),
    processed_data_path: InputPath(),
):
    import os
    import joblib
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import classification_report, confusion_matrix

    # Load model and test data
    model = joblib.load(os.path.join(model_input_path, 'model.joblib'))
    X_test = joblib.load(os.path.join(model_input_path, 'X_test.pkl'))
    y_test = joblib.load(os.path.join(model_input_path, 'y_test.pkl'))

    # Load label encoder
    label_encoder = joblib.load(os.path.join(processed_data_path, 'label_encoder.joblib'))

    # Predict on test data
    y_pred = model.predict(X_test)

    # Ensure y_test and y_pred are 1D arrays
    y_test = np.array(y_test).flatten()
    y_pred = np.array(y_pred).flatten()

    # Map numerical labels back to category names
    label_mapping = dict(zip(label_encoder.transform(label_encoder.classes_), label_encoder.classes_))
    y_test_labels = [label_mapping[label] for label in y_test]
    y_pred_labels = [label_mapping[label] for label in y_pred]

    # Debugging prints
    print("y_test_labels type:", type(y_test_labels))
    print("y_pred_labels type:", type(y_pred_labels))
    print("y_test_labels length:", len(y_test_labels))
    print("y_pred_labels length:", len(y_pred_labels))
    print("Unique labels in y_test_labels:", np.unique(y_test_labels))
    print("Unique labels in y_pred_labels:", np.unique(y_pred_labels))

    # Classification report
    print("Classification Report:")
    print(classification_report(y_test_labels, y_pred_labels))

