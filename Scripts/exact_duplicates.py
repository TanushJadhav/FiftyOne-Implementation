#!/usr/bin/env python3

import fiftyone.brain as fob
import argparse
import fiftyone as fo

from read_dataset import load_dataset
from delete_images import track_deleted_images

def detect_duplicates(dataset_dir, name, dataset_type):
    # Load dataset using the function from load_fiftyone_dataset.py
    dataset = load_dataset(dataset_dir, name, dataset_type)

    # Compute exact duplicates
    duplicates_map = fob.compute_exact_duplicates(dataset)
    
    flag = 1

    if not duplicates_map:
        print("No duplicate images exist in the dataset.")
        flag=0
    else:
        print("Duplicate images found:")
        print(duplicates_map)

    return dataset, flag

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect duplicate images in a FiftyOne dataset.")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset")
    parser.add_argument("--dataset_dir", type=str, required=True, help="Path to the dataset directory")
    parser.add_argument(
        "--dataset_type", type=str, default="ImageDirectory", 
        choices=["ImageDirectory", "VideoDirectory", "ImageDirectoryTree", "VideoDirectoryTree", "yoloDataset"], 
        help="Type of the dataset (default: ImageDirectory)"
    )

    args = parser.parse_args()

    # Detect duplicates and get the dataset
    dataset, flag = detect_duplicates(args.dataset_dir, args.name, args.dataset_type)

    # Launch the FiftyOne App (moved outside the function)
    if flag==1:
        # Store original file paths before launching FiftyOne
        original_filepaths = {s.filepath for s in dataset}

        # Launch the FiftyOne App
        session = fo.launch_app(dataset, address="0.0.0.0")

        try:
            session.wait()  # Wait for user interaction
        finally:
            # Track and save deleted images after session closes
            track_deleted_images(dataset, original_filepaths)
