# n06_upload_to_s3_component.py

import kfp
from kfp import dsl
from kfp.dsl import component, InputPath

@component(
    packages_to_install=['boto3'],
)
def upload_to_s3_component(
    directory_path: InputPath(),
    bucket_name: str,
    s3_prefix: str,
    endpoint_url: str = 'http://minio:9000',
    aws_access_key_id: str = 'minio',
    aws_secret_access_key: str = 'minio123',
    region_name: str = 'us-east-1',
):
    import boto3
    import logging
    import os
    from botocore.exceptions import NoCredentialsError, ClientError

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    def upload_directory_to_s3(directory_path, bucket_name, s3_prefix):
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
        )
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, directory_path)
                s3_key = os.path.join(s3_prefix, relative_path)
                try:
                    s3.upload_file(local_path, bucket_name, s3_key)
                    logging.info(f"Uploaded {local_path} to s3://{bucket_name}/{s3_key}")
                except Exception as e:
                    logging.error(f"Failed to upload {local_path}: {e}")

    upload_directory_to_s3(directory_path, bucket_name, s3_prefix)
    logging.info("Upload completed.")
