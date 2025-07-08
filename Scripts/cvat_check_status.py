#!/usr/bin/env python3

import fiftyone as fo
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and merge annotations into a FiftyOne dataset.")
    parser.add_argument("--anno_key", type=str, required=True, help="Annotation key used for annotations")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset")

    args = parser.parse_args()

    # Load dataset
    dataset = fo.load_dataset(args.name)

    # Merge annotations into dataset
    dataset.load_annotations(args.anno_key)
    
    print(dataset.first().detections) 

    # Load the annotation view
    # dataset.load_annotation_view(args.anno_key)

    # Launch FiftyOne App
    session = fo.launch_app(dataset, address="0.0.0.0")
    session.wait()
