import os
import joblib
import argparse
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType, StringTensorType
from sklearn.pipeline import Pipeline

def load_model(model_path):
    model = joblib.load(model_path)
    print(f"Model loaded from {model_path}")
    return model

def load_preprocessor(preprocessor_path):
    preprocessor = joblib.load(preprocessor_path)
    print(f"Preprocessor loaded from {preprocessor_path}")
    return preprocessor

def export_model_to_onnx(pipeline, output_path, initial_type):
    onnx_model = convert_sklearn(pipeline, initial_types=initial_type, target_opset=12)
    with open(output_path, 'wb') as f:
        f.write(onnx_model.SerializeToString())
    print(f"Model exported to ONNX format at {output_path}")

def get_feature_details(preprocessor):
    feature_details = []
    for transformer in preprocessor.transformers_:
        transformer_name, transformer_object, columns = transformer
        for column in columns:
            if column in ['proto', 'service', 'state']:
                feature_details.append((column, StringTensorType([None, 1])))
            else:
                feature_details.append((column, FloatTensorType([None, 1])))
    return feature_details

def main():
    parser = argparse.ArgumentParser(description="Export Predictive Model to ONNX Format")
    parser.add_argument('--model_path', type=str, default='./models/predictive_model/model.joblib', help='Path to the trained model file (default: "./models/predictive_model/model.joblib")')
    parser.add_argument('--preprocessor_path', type=str, default='./data/processed/preprocessor.pkl', help='Path to the preprocessor file (default: "./data/processed/preprocessor.pkl")')
    parser.add_argument('--output_dir', type=str, default='./models/predictive_model', help='Directory to save the ONNX model (default: "./models/predictive_model")')
    parser.add_argument('--onnx_model_filename', type=str, default='model.onnx', help='Filename for the ONNX model (default: "model.onnx")')

    args = parser.parse_args()

    model = load_model(args.model_path)
    preprocessor = load_preprocessor(args.preprocessor_path)

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    initial_type = get_feature_details(preprocessor)

    output_path = os.path.join(args.output_dir, args.onnx_model_filename)
    export_model_to_onnx(pipeline, output_path, initial_type)

if __name__ == "__main__":
    main()
