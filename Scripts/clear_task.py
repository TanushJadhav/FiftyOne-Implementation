#!/usr/bin/env python3

import fiftyone as fo
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and manage annotations in a FiftyOne dataset.")
    parser.add_argument("--anno_key", type=str, required=True, help="Annotation key used for annotations")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset")
    parser.add_argument("--delete_task", type=bool, default=False, help="Delete task from CVAT (default: False)")

    args = parser.parse_args()

    # Load dataset
    dataset = fo.load_dataset(args.name)
    dataset.load_annotations(args.anno_key)

    if args.delete_task:
        # Delete tasks from CVAT
        results = dataset.load_annotation_results(args.anno_key)
        results.cleanup()

    # Delete annotation run record (not the labels) from FiftyOne
    dataset.delete_annotation_run(args.anno_key)
