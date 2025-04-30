#!/usr/bin/env python3
"""
download.py: Function-based downloader for Kaggle datasets via CLI.

Place this file alongside your `result.ipynb` in the `dsci_final_data` folder.
Ensure `kaggle.json` is also in this folder with permissions set (`chmod 600 kaggle.json`).
"""
import os
import subprocess
from pathlib import Path

# List of Kaggle datasets to fetch
DATASETS = [
    "mrmars1010/iphone-customer-reviews-nlp",
    "thedevastator/apple-iphone-11-reviews-from-amazon-com",
]

# Project root (dsci_final_data)
PROJECT_ROOT = Path(__file__).parent.resolve()


def download_kaggle_datasets():
    """
    Download and extract each dataset in DATASETS into PROJECT_ROOT.
    Uses the Kaggle CLI under the hood.
    """
    # 1️⃣ Verify kaggle.json exists and is secure
    token = PROJECT_ROOT / "kaggle.json"
    if not token.exists():
        raise FileNotFoundError(f"kaggle.json not found in {PROJECT_ROOT}")
    token.chmod(0o600)

    # 2️⃣ Tell Kaggle CLI where to look for credentials
    os.environ["KAGGLE_CONFIG_DIR"] = str(PROJECT_ROOT)

    # 3️⃣ Download & extract each dataset
    for ds in DATASETS:
        print(f"Downloading {ds} to {PROJECT_ROOT}...")
        subprocess.run([
            "kaggle", "datasets", "download", "-d", ds,
            "-p", str(PROJECT_ROOT)
        ], check=True)

        # Unzip plus cleanup
        slug = ds.split("/")[1]
        archive = PROJECT_ROOT / f"{slug}.zip"
        if archive.exists():
            print(f"Extracting {archive}...")
            subprocess.run([
                "unzip", "-o", str(archive), "-d", str(PROJECT_ROOT)
            ], check=True)
            archive.unlink()
            print(f"Removed archive: {archive.name}\n")
        else:
            print(f"Warning: {archive.name} not found after download.")

    print("All Kaggle datasets downloaded and extracted.")


if __name__ == '__main__':
    download_kaggle_datasets()

# ------------------------------------------
# Usage in result.ipynb:
# ------------------------------------------
# In a notebook cell:
#
# ```python
# from download import download_kaggle_datasets
# download_kaggle_datasets()
# ```
#
# This will download both datasets directly into the `dsci_final_data` folder and extract them there.

