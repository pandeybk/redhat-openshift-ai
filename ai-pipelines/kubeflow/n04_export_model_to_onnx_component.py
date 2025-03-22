# n04_export_model_to_onnx_component.py

import kfp
from kfp import dsl
from kfp.dsl import component, InputPath, OutputPath

@component(
    packages_to_install=['scikit-learn', 'joblib', 'skl2onnx', 'onnx', 'pandas'],
)
def export_model_to_onnx_component(
    model_input_path: InputPath(),
    processed_data_path: InputPath(),
    onnx_model_output_path: OutputPath(),
):
    import os
    import joblib
    import pandas as pd
    import numpy as np
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType
    import onnx

    # Load model
    model = joblib.load(os.path.join(model_input_path, 'model.joblib'))

    # Load sample input to get feature shape
    X = pd.read_pickle(os.path.join(processed_data_path, 'X.pkl'))
    X_values = X.values.astype(np.float32)
    n_features = X_values.shape[1]

    # Define the initial type
    initial_type = [('float_input', FloatTensorType([None, n_features]))]

    # Set options to ensure all components are included
    options = {id(model): {'zipmap': False}}

    # Convert the model
    onnx_model = convert_sklearn(model, initial_types=initial_type, options=options, target_opset=12)

    # Apply the patch directly to the ONNX model
    for output in onnx_model.graph.output:
        if output.name == "label":
            # Ensure the first dimension exists for dynamic batch size
            if len(output.type.tensor_type.shape.dim) < 1:
                output.type.tensor_type.shape.dim.add()  # Add a new dimension
            output.type.tensor_type.shape.dim[0].dim_param = "batch_size"  # Dynamic batch size

            # Ensure the second dimension exists for scalar output
            if len(output.type.tensor_type.shape.dim) < 2:
                output.type.tensor_type.shape.dim.add()  # Add a new dimension
            output.type.tensor_type.shape.dim[1].dim_value = 1  # Fixed scalar output

    # Save the patched ONNX model
    os.makedirs(onnx_model_output_path, exist_ok=True)
    # Create the directory structure
    model_dir = os.path.join(onnx_model_output_path, '1')
    os.makedirs(model_dir, exist_ok=True)
    onnx_model_path = os.path.join(model_dir, 'model.onnx')
    with open(onnx_model_path, 'wb') as f:
        f.write(onnx_model.SerializeToString())

    # Create config.pbtxt
    config_pbtxt_content = '''
    name: "netsentinel"
    platform: "onnxruntime_onnx"
    max_batch_size: 8
    output [
      {
        name: "label"
        data_type: TYPE_INT64
        dims: [1] 
      },
      {
        name: "probabilities"
        data_type: TYPE_FP32
        dims: [11] 
      }
    ]
    '''
    config_pbtxt_path = os.path.join(onnx_model_output_path, 'config.pbtxt')
    with open(config_pbtxt_path, 'w') as f:
        f.write(config_pbtxt_content.strip())

    print(f"RandomForestClassifier model exported to ONNX format with patched output shape at {onnx_model_path}")
    print(f"Config.pbtxt file created at {config_pbtxt_path}")
