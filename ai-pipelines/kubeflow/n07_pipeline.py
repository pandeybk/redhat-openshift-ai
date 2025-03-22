# n07_pipeline.py

import kfp
from kfp import dsl

from n01_download_dataset_component import download_dataset_component
from n02_preprocess_data_component import preprocess_data_component
from n03_train_model_component import train_model_component
from n04_export_model_to_onnx_component import export_model_to_onnx_component
from n05_evaluate_model_component import evaluate_model_component
from n06_upload_to_s3_component import upload_to_s3_component
import uuid

@dsl.pipeline(
    name='Predictive Model Pipeline',
    description='A pipeline that downloads data, preprocesses it, trains a model, evaluates it, exports it to ONNX format, and uploads it to S3.'
)
def predictive_model_pipeline(
    dataset: str = 'mrwellsdavid/unsw-nb15',
    bucket_name: str = 'predictive-model-training',
    endpoint_url: str = 'http://minio-service.netsentinel:9000',
    aws_access_key_id: str = 'minio',
    aws_secret_access_key: str = 'minio123',
    region_name: str = 'us-east-1',
):
    # Generate s3_prefix using run ID
    s3_prefix = f'netsentinel/{uuid.uuid4()}/'

    # Step 1: Download dataset
    download_task = download_dataset_component(
        dataset=dataset,
    )

    # Mount the Kaggle secret as a volume
    kaggle_secret_name = 'kaggle-secret'  # The name of your Kubernetes Secret

    # Use kubernetes.use_secret_as_volume to mount the secret
    from kfp import kubernetes

    kubernetes.use_secret_as_volume(
        task=download_task,
        secret_name=kaggle_secret_name,
        mount_path='/.config/kaggle',  # Kaggle API expects kaggle.json here
    )

    # Step 2: Preprocess data
    preprocess_task = preprocess_data_component(
        raw_data_path=download_task.outputs['download_path'],
    )

    # Step 3: Train model
    train_task = train_model_component(
        processed_data_path=preprocess_task.outputs['processed_data_path'],
    )

    # Step 4: Export model to ONNX
    export_task = export_model_to_onnx_component(
        model_input_path=train_task.outputs['model_output_path'],
        processed_data_path=preprocess_task.outputs['processed_data_path'],
    )

    # Step 5: Evaluate model
    evaluate_task = evaluate_model_component(
        model_input_path=train_task.outputs['model_output_path'],
        processed_data_path=preprocess_task.outputs['processed_data_path'],
    )

    # Step 6: Upload to S3
    upload_task = upload_to_s3_component(
        directory_path=export_task.outputs['onnx_model_output_path'],
        bucket_name=bucket_name,
        s3_prefix=s3_prefix,
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

if __name__ == '__main__':
    from kfp import compiler
    compiler.Compiler().compile(predictive_model_pipeline, 'predictive_model_pipeline.yaml')
