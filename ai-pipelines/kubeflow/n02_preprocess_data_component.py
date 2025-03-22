import kfp
from kfp import dsl
from kfp.dsl import component, InputPath, OutputPath

@component(
    packages_to_install=['pandas', 'numpy', 'scikit-learn', 'joblib'],
)
def preprocess_data_component(
    raw_data_path: InputPath(),
    processed_data_path: OutputPath(),
):
    import os
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import OrdinalEncoder, StandardScaler, LabelEncoder
    import joblib

    # List files in raw_data_path
    print(f"Files in raw_data_path: {os.listdir(raw_data_path)}")

    # Read the features file to get the column names
    features_file = os.path.join(raw_data_path, "NUSW-NB15_features.csv")
    if not os.path.exists(features_file):
        raise FileNotFoundError(f"Features file not found at {features_file}")
    features = pd.read_csv(features_file, encoding='cp1252')
    feature_names = features['Name'].tolist()

    # Read UNSW-NB15 CSV files
    csv_files = [os.path.join(raw_data_path, f"UNSW-NB15_{i}.csv") for i in range(1, 5)]
    dataframes = []
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Data file not found: {csv_file}")
        print(f"Reading {csv_file}")
        df = pd.read_csv(csv_file, header=None, names=feature_names, encoding='latin1', low_memory=False)
        dataframes.append(df)
        print(f"Loaded {csv_file} with shape {df.shape}")

    # Concatenate dataframes
    train_df = pd.concat(dataframes, ignore_index=True)
    print(f"Dataset shape after concatenation: {train_df.shape}")

    # Shuffle the data
    train_df = train_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Remove duplicates
    train_df = train_df.drop_duplicates()
    print(f"Dataset shape after removing duplicates: {train_df.shape}")

    # Explicitly define columns to exclude
    columns_to_exclude = ['srcip', 'sport', 'dstip', 'dsport', 'Stime', 'Ltime', 'Label', 'attack_cat']

    # Define categorical columns (excluding columns_to_exclude)
    categorical_cols = [
        'proto', 'state', 'service',
        'ct_ftp_cmd',  # If you decide to treat this as categorical
    ]

    # Ensure these columns are treated as strings
    train_df[categorical_cols] = train_df[categorical_cols].astype(str)

    # Handle missing values in categorical columns
    train_df[categorical_cols] = train_df[categorical_cols].fillna('Unknown')

    # Handle missing values in numerical columns
    numerical_cols = [col for col in train_df.columns if col not in categorical_cols + columns_to_exclude]
    train_df[numerical_cols] = train_df[numerical_cols].fillna(train_df[numerical_cols].median())
    print("Missing values handled.")

    # Fix spaces in attack_cat and handle missing values
    if 'attack_cat' in train_df.columns:
        train_df['attack_cat'] = train_df['attack_cat'].str.strip()  # Remove leading and trailing spaces
        train_df['attack_cat'] = train_df['attack_cat'].fillna('Unknown')  # Replace missing values with 'Unknown'

    # Explicitly reorder 'attack_cat' so 'Unknown' is first
    categories = train_df['attack_cat'].unique().tolist()
    categories.remove('Unknown')
    categories = ['Unknown'] + sorted(categories)
    train_df['attack_cat'] = pd.Categorical(train_df['attack_cat'], categories=categories, ordered=True)
    print(f"Unique values in attack_cat after ordering: {train_df['attack_cat'].unique()}")

    # Encode categorical variables using OrdinalEncoder
    ordinal_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
    train_df[categorical_cols] = ordinal_encoder.fit_transform(train_df[categorical_cols])
    print(f"Categorical variables encoded using OrdinalEncoder: {categorical_cols}")

    # Separate features and target
    X = train_df.drop(columns=columns_to_exclude)
    y = train_df['attack_cat']

    # Encode target variable explicitly ensuring 'Unknown' is 0
    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.array(categories)  # Explicitly set the order of classes
    y_encoded = label_encoder.transform(y)
    print("Target variable encoded.")

    # Display the class mapping
    class_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
    print(f"Class mapping: {class_mapping}")

    # Scale numerical features
    scaler = StandardScaler()
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    print("Numerical features scaled.")

    # Save preprocessed data and encoders
    os.makedirs(processed_data_path, exist_ok=True)
    X.to_pickle(os.path.join(processed_data_path, 'X.pkl'))
    joblib.dump(y_encoded, os.path.join(processed_data_path, 'y_encoded.pkl'))
    joblib.dump(ordinal_encoder, os.path.join(processed_data_path, 'ordinal_encoder.joblib'))
    joblib.dump(scaler, os.path.join(processed_data_path, 'scaler.joblib'))
    joblib.dump(label_encoder, os.path.join(processed_data_path, 'label_encoder.joblib'))
    print(f"Processed data and encoders saved to {processed_data_path}")
