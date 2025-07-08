#!/bin/bash

# Change directory to the Scripts folder
cd /home/tanush-jadhav/Desktop/Voxel_51/Scripts || { echo "Directory not found!"; exit 1; }

# Function to load dataset to CVAT
load_dataset_to_cvat() {
    echo "Loading dataset to CVAT..."
    python3 cvat_load_dataset.py --name "$name" --anno_key "$anno_key" --dataset_dir "$dataset_dir" --dataset_type "$dataset_type" --label_field "$label_field" --label_type "$label_type" --classes "$classes"
}

# Function to check CVAT status
check_cvat_status() {
    echo "Checking CVAT status..."
    python3 cvat_check_status.py --name "$name" --anno_key "$anno_key"
}

# Function to clear task in CVAT
clear_task() {
    echo "Clearing task for dataset: $name"
    read -p "Do you also want to delete the task from CVAT? (y/n): " delete_choice
    if [[ "$delete_choice" == "y" || "$delete_choice" == "Y" ]]; then
        python3 clear_task.py --name "$name" --delete_task
    else
        python3 clear_task.py --name "$name"
    fi
}

# Prompt the user for their choice
echo "What would you like to do?"
echo "1. Load Dataset to CVAT"
echo "2. Check CVAT Status in FiftyOne"
echo "3. Clear a Task"
read -p "Enter your choice (1-3): " choice

# Load dataset to CVAT
if [ "$choice" -eq 1 ]; then
    read -p "Enter dataset name (Remember the Name): " name
    read -p "Enter annotation key (Remember the Key): " anno_key
    read -p "Enter dataset directory: " dataset_dir

    # Choose dataset type
    echo "Choose dataset type from the following options:"
    options=("ImageDirectory" "VideoDirectory" "ImageDirectoryTree" "VideoDirectoryTree" "yoloDataset")
    select dataset_type in "${options[@]}"; do
        [[ -n "$dataset_type" ]] && break
        echo "Invalid choice. Try again."
    done

    # Choose label field
    echo "Choose label field from the following options:"
    label_fields=("detections" "segmentations" "keypoints" "polygons" "classifications")
    select label_field in "${label_fields[@]}"; do
        [[ -n "$label_field" ]] && break
        echo "Invalid choice. Try again."
    done

    # Choose label type
    echo "Choose label type from the following options:"
    label_types=("detections" "instances" "polylines" "keypoints")
    select label_type in "${label_types[@]}"; do
        [[ -n "$label_type" ]] && break
        echo "Invalid choice. Try again."
    done

    # Ask for class names
    read -p "Enter class names (comma-separated): " classes

    load_dataset_to_cvat
fi

# Check CVAT Status
if [ "$choice" -eq 2 ]; then
    read -p "Enter dataset name: " name
    read -p "Enter annotation key: " anno_key
    check_cvat_status
fi

# Clear a task
if [ "$choice" -eq 3 ]; then
    read -p "Enter dataset name: " name
    clear_task
fi

