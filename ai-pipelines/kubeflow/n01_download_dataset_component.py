# n01_download_dataset_component.py

import kfp
from kfp import dsl
from kfp.dsl import component, OutputPath

@component(
    packages_to_install=['kaggle'],
)
def download_dataset_component(
    dataset: str,
    download_path: OutputPath(),
):
    import os
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print(f"Downloading dataset '{dataset}'...")
    api.dataset_download_files(dataset, path=download_path, unzip=True)

    print(f"Dataset downloaded and extracted to '{download_path}'.")
    print(f"Files in download_path: {os.listdir(download_path)}")
