import os
import zipfile
import argparse
from kaggle.api.kaggle_api_extended import KaggleApi

def download_and_extract_kaggle_dataset(dataset, download_path):
    """
    Downloads and extracts a Kaggle dataset.

    Args:
        dataset (str): Kaggle dataset identifier.
        download_path (str): Path to download and extract the dataset.
    """
    api = KaggleApi()
    api.authenticate()

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print(f"Downloading dataset '{dataset}'...")
    api.dataset_download_files(dataset, path=download_path, unzip=True)
    print(f"Dataset downloaded and extracted to '{download_path}'.")

def main():
    parser = argparse.ArgumentParser(description="Download and Extract Dataset from Kaggle")
    parser.add_argument('--dataset', type=str, default='mrwellsdavid/unsw-nb15', help='Kaggle dataset identifier (default: "mrwellsdavid/unsw-nb15")')
    parser.add_argument('--download_path', type=str, default='./data/raw', help='Directory to download and extract the dataset (default: "./data/raw")')
    
    args = parser.parse_args()

    download_and_extract_kaggle_dataset(args.dataset, args.download_path)

if __name__ == "__main__":
    main()
