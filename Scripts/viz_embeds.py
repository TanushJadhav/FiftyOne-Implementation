#!/usr/bin/env python3

import os
import cv2
import numpy as np
import fiftyone as fo
import fiftyone.brain as fob
import fiftyone.zoo as foz
from sklearn.decomposition import PCA
import argparse

from read_dataset import load_dataset
from delete_images import track_deleted_images

def resize_image(image, max_size=512):
    """Resize image while preserving aspect ratio."""
    h, w = image.shape[:2]
    scale = min(max_size / h, max_size / w)  # Scale factor to keep aspect ratio
    new_h, new_w = int(h * scale), int(w * scale)
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

def compute_pca_embeddings(dataset_dir, name, dataset_type, max_size=512, n_components=512):
    """Compute PCA embeddings for a dataset of images."""
    # Load dataset
    dataset = load_dataset(dataset_dir, name, dataset_type)

    # Read images, resize, and find the max number of pixels
    image_arrays = []
    max_pixels = 0

    for f in dataset.values("filepath"):
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)  # Read in grayscale
        img_resized = resize_image(img, max_size=max_size)  # Resize while keeping aspect ratio
        img_flattened = img_resized.ravel()  # Flatten to 1D array
        image_arrays.append(img_flattened)
        max_pixels = max(max_pixels, img_flattened.shape[0])  # Track max pixels

    # Pad images to ensure all embeddings have the same length
    padded_embeddings = np.array([
        np.pad(img, (0, max_pixels - img.shape[0])) for img in image_arrays
    ])

    print("Resized embeddings shape:", padded_embeddings.shape)  # Should be (num_samples, max_pixels)

    # Apply PCA to reduce dimensionality before UMAP
    n_components = min(n_components, padded_embeddings.shape[0])  # Ensure n_components is <= number of samples
    pca = PCA(n_components=n_components)
    pca_embeddings = pca.fit_transform(padded_embeddings)

    print("PCA-reduced embeddings shape:", pca_embeddings.shape)  # (num_samples, n_components)

    return pca_embeddings, dataset
    return pca_embeddings

def compute_embeddings(dataset_dir, name, dataset_type, choice):
    
    if choice=="pixel_embeddings":

        pca_embeddings, dataset = compute_pca_embeddings(args.dataset_dir, args.name, args.dataset_type)
        results = fob.compute_visualization(
            dataset,
            embeddings=pca_embeddings,
            num_dims=2,
            method="umap",
            brain_key=choice,
            verbose=True,
            seed=42
        )
    else:
        # Load dataset
        dataset = load_dataset(dataset_dir, name, dataset_type)

        model = {"resnet_embeddings": "resnet50-imagenet-torch", "clip_embeddings": "clip-vit-base32-torch", "inception_embeddings": "inception-v3-imagenet-torch"}
        
        res = fob.compute_visualization(
            dataset,
            model=model[choice],
            embeddings=choice, 
            method="umap",
            brain_key=choice,
            batch_size=10
        )

    uniqueness = fob.compute_uniqueness(
        dataset,
        embeddings=choice
    )

    representativeness = fob.compute_representativeness(
        dataset,
        embeddings=choice
    )

    
    return dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute image embeddings and visualize them using UMAP.")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset")
    parser.add_argument("--dataset_dir", type=str, required=True, help="Path to the dataset directory")
    parser.add_argument(
        "--dataset_type", type=str, default="ImageDirectory", 
        choices=["ImageDirectory", "VideoDirectory", "ImageDirectoryTree", "VideoDirectoryTree", "yoloDataset"], 
        help="Type of the dataset (default: ImageDirectory)"
    )
    parser.add_argument(
        "--embedding_type", type=str, default="resnet", 
        choices=["pixel", "resnet", "clip", "inception"], 
        help="Type of Model to extract Embeddings"
    )

    args = parser.parse_args()

    embed_dict = {"pixel": "pixel_embeddings", "resnet": "resnet_embeddings", "clip": "clip_embeddings", "inception": "inception_embeddings"}

    # Compute embeddings and get the dataset
    dataset = compute_embeddings(args.dataset_dir, args.name, args.dataset_type, embed_dict[args.embedding_type])

    # Store original file paths before launching FiftyOne
    original_filepaths = {s.filepath for s in dataset}

    # Launch the FiftyOne App
    session = fo.launch_app(dataset, address="0.0.0.0")

    try:
        session.wait()  # Wait for user interaction
    finally:
        # Track and save deleted images after session closes
        track_deleted_images(dataset, original_filepaths)
