import os
import boto3
import argparse
import logging
from botocore.exceptions import NoCredentialsError

def setup_logging(log_level):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def upload_to_s3(file_path, bucket_name, s3_key):
    """
    Upload a file to an S3 (or S3-compatible) bucket.

    This version:
      - Reads credentials from environment variables:
         AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
      - Reads endpoint from environment variable:
         AWS_S3_ENDPOINT (e.g., http://minio-service.netsentinel:9000)
    """

    # Pull environment variables if set
    region_name = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')  # Default to 'us-east-1'
    endpoint_url = os.getenv('AWS_S3_ENDPOINT')                 # No default; only set if present
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    try:
        # Create the S3 client, explicitly passing endpoint and credentials if provided
        s3 = boto3.client(
            's3',
            region_name=region_name,
            endpoint_url=endpoint_url,  # For MinIO or other non-AWS endpoints
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # Attempt the file upload
        s3.upload_file(file_path, bucket_name, s3_key)
        s3_url = f"s3://{bucket_name}/{s3_key}"
        logging.info(f"File uploaded to S3: {s3_url}")
        return s3_url

    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return None
    except NoCredentialsError:
        logging.error("AWS credentials not available. (Check environment variables or ~/.aws/credentials)")
        return None
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Upload file to S3 or S3-compatible storage")
    parser.add_argument('--file_path', type=str, default='./models/predictive_model/model.onnx',
                        help='Path to the file to upload (default: "./models/predictive_model/model.onnx")')
    parser.add_argument('--bucket_name', type=str, default=os.getenv('AWS_S3_BUCKET', 'predictive-model-training'),
                        help='S3 bucket name (default: "predictive-model-training" or AWS_S3_BUCKET env var)')
    parser.add_argument('--s3_key', type=str, default='elyra/model.onnx',
                        help='S3 key for the uploaded file (default: "elyra/model.onnx")')
    parser.add_argument('--log_level', type=str, default='DEBUG',
                        help='Log level (default: INFO)')
    args = parser.parse_args()

    setup_logging(args.log_level)

    s3_url = upload_to_s3(args.file_path, args.bucket_name, args.s3_key)
    if s3_url:
        logging.info(f"Upload successful. File available at {s3_url}")
    else:
        logging.error("Upload failed.")

if __name__ == "__main__":
    main()
