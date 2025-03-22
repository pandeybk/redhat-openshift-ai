import os
import joblib
import argparse
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    roc_auc = roc_auc_score(y_test, y_proba)
    print(f"ROC AUC Score: {roc_auc:.4f}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate Predictive Model")
    parser.add_argument('--model_path', type=str, default='./models/predictive_model/model.joblib', help='Path to the trained model file (default: "./models/predictive_model/model.joblib")')
    parser.add_argument('--input_dir', type=str, default='./data/processed', help='Directory containing test data (default: "./data/processed")')
    
    args = parser.parse_args()

    X_test = joblib.load(os.path.join(args.input_dir, 'X_test.pkl'))
    y_test = joblib.load(os.path.join(args.input_dir, 'y_test.pkl'))
    model = joblib.load(args.model_path)

    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()
