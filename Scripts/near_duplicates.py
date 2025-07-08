#!/usr/bin/env python3

import fiftyone as fo
import fiftyone.brain as fob
import argparse

from read_dataset import load_dataset
from delete_images import track_deleted_images

def detect_near_duplicates(dataset_dir, name, dataset_type, threshold):
    # Load the dataset using the function from load_fiftyone_dataset.py
    dataset = load_dataset(dataset_dir, name, dataset_type)

    # Compute near duplicates
    index = fob.compute_near_duplicates(dataset, threshold=threshold)

    dups_view = None  # Initialize with a default value

    if not index.duplicate_ids:
        print("There are No Duplicate Images in your Dataset to display.")
    else:
        dups_view = index.duplicates_view(
            type_field="dup_type",
            dist_field="dup_dist"
        )

    return dups_view

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect near duplicate images in a FiftyOne dataset.")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset")
    parser.add_argument("--dataset_dir", type=str, required=True, help="Path to the dataset directory")
    parser.add_argument(
        "--dataset_type", type=str, default="ImageDirectory", 
        choices=["ImageDirectory", "VideoDirectory", "ImageDirectoryTree", "VideoDirectoryTree", "yoloDataset"], 
        help="Type of the dataset (default: ImageDirectory)"
    )
    parser.add_argument("--threshold", type=float, default=0.02, help="Threshold for near duplicate detection (default: 0.02)")

    args = parser.parse_args()

    # Detect duplicates
    dups_view = detect_near_duplicates(args.dataset_dir, args.name, args.dataset_type, args.threshold)

    if dups_view is not None:
        # Store original file paths before launching FiftyOne
        original_filepaths = {s.filepath for s in dups_view}

        # Launch the FiftyOne App
        session = fo.launch_app(dups_view, address="0.0.0.0")

        try:
            session.wait()  # Wait for user interaction
        finally:
            # Track and save deleted images after session closes
            track_deleted_images(dups_view, original_filepaths)
