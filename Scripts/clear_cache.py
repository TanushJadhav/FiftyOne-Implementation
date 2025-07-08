#!/usr/bin/env python3

import argparse
import fiftyone as fo

def delete_dataset(dataset_name):
    """Delete a dataset from FiftyOne."""
    try:
        fo.delete_dataset(dataset_name)
        print(f"Dataset '{dataset_name}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Delete a FiftyOne dataset by name.")
    parser.add_argument("dataset_name", type=str, help="The name of the dataset to delete")

    # Parse command-line arguments
    args = parser.parse_args()

    # Delete the specified dataset
    delete_dataset(args.dataset_name)
