import os
import joblib
import argparse
from sklearn.ensemble import RandomForestClassifier

def train_model(X_train, y_train, n_estimators, random_state, n_jobs):
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, n_jobs=n_jobs)
    model.fit(X_train, y_train)
    print("Model training completed successfully.")
    return model

def save_model(model, output_dir, model_filename):
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, model_filename)
    joblib.dump(model, model_path)
    print(f"Model saved at {model_path}")

def main():
    parser = argparse.ArgumentParser(description="Train Predictive Model")
    parser.add_argument('--input_dir', type=str, default='./data/processed', help='Directory containing preprocessed data (default: "./data/processed")')
    parser.add_argument('--output_dir', type=str, default='./models/predictive_model', help='Directory to save the trained model (default: "./models/predictive_model")')
    parser.add_argument('--n_estimators', type=int, default=100, help='Number of trees in the Random Forest (default: 100)')
    parser.add_argument('--random_state', type=int, default=42, help='Random state for reproducibility (default: 42)')
    parser.add_argument('--n_jobs', type=int, default=-1, help='Number of parallel jobs for training (default: -1)')
    
    args = parser.parse_args()

    X_train = joblib.load(os.path.join(args.input_dir, 'X_train.pkl'))
    y_train = joblib.load(os.path.join(args.input_dir, 'y_train.pkl'))
    
    model = train_model(X_train, y_train, args.n_estimators, args.random_state, args.n_jobs)
    save_model(model, args.output_dir, 'model.joblib')

if __name__ == "__main__":
    main()
