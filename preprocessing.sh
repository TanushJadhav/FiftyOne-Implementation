#!/bin/bash

cd /home/tanush-jadhav/Desktop/Voxel_51/Scripts || { echo "Directory not found!"; exit 1; }

# Function to view dataset
view_dataset() {
    echo "Viewing the dataset..."
    python3 read_dataset.py --name "$dataset_name" --dataset_dir "$dataset_dir" --dataset_type "$dataset_type"
}

# Function to get embeddings
get_embeddings() {
    echo "Getting embeddings..."
    python3 viz_embeds.py --name "$dataset_name" --dataset_dir "$dataset_dir" --dataset_type "$dataset_type" --embedding_type "$embedding_type"
}

# Function to get near duplicates
get_near_duplicates() {
    echo "Getting near duplicates..."
    python3 near_duplicates.py --name "$dataset_name" --dataset_dir "$dataset_dir" --dataset_type "$dataset_type"
}

# Function to get exact duplicates
get_exact_duplicates() {
    echo "Getting exact duplicates..."
    python3 exact_duplicates.py --name "$dataset_name" --dataset_dir "$dataset_dir" --dataset_type "$dataset_type"
}

# Function to delete a dataset
delete_dataset() {
    echo "Deleting the dataset..."
    python3 clear_cache.py "$dataset_name"
}

# Prompt the user for their choice
echo "What would you like to do?"
echo "1. View Dataset"
echo "2. Get Embeddings"
echo "3. Get Near Duplicates"
echo "4. Get Exact Duplicates"
echo "5. Delete Dataset"
read -p "Enter your choice (1-5): " choice

# Prompt for dataset name
read -p "Enter dataset name: " dataset_name

# If deleting dataset, no need for further inputs
if [ "$choice" -eq 5 ]; then
    delete_dataset
    exit 0
fi

# Prompt for dataset directory
read -p "Enter dataset directory (Provide Absolute Path): " dataset_dir

# Choose dataset type from available options
echo "Choose dataset type from the following options:"
echo "1. ImageDirectory - Use When all images are in the Directory mentioned above"
echo "2. VideoDirectory - Use When all videos are in the Directory mentioned above"
echo "3. ImageDirectoryTree - Use when images are in subfolders in the Directory Mentioned above"
echo "4. VideoDirectoryTree  - Use when videos are in subfolders in the Directory Mentioned above"
echo "5. CocoDataset - To Import COCO Dataset to FiftyOne"
echo "6. YoloV5Dataset - To Import yoloV5 Dataset to FiftyOne"
read -p "Enter your choice (1-6): " dataset_type_choice

case $dataset_type_choice in
    1) dataset_type="ImageDirectory" ;;
    2) dataset_type="VideoDirectory" ;;
    3) dataset_type="ImageDirectoryTree" ;;
    4) dataset_type="VideoDirectoryTree" ;;
    5) dataset_type="CocoDataset" ;;
    6) dataset_type="YoloV5Dataset" ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

# If the choice is for embeddings, ask for embedding type
if [ "$choice" -eq 2 ]; then
    echo "Choose embedding type from the following options:"
    echo "1. pixel"
    echo "2. resnet"
    echo "3. clip"
    echo "4. inception"
    read -p "Enter your choice (1-4): " embedding_type_choice

    case $embedding_type_choice in
        1) embedding_type="pixel" ;;
        2) embedding_type="resnet" ;;
        3) embedding_type="clip" ;;
        4) embedding_type="inception" ;;
        *)
            echo "Invalid choice. Exiting..."
            exit 1
            ;;
    esac
fi

# Run the corresponding Python script based on user choice
case $choice in
    1)
        view_dataset
        ;;
    2)
        get_embeddings
        ;;
    3)
        get_near_duplicates
        ;;
    4)
        get_exact_duplicates
        ;;
    5)
        delete_dataset
        ;;
    *)
        echo "Invalid choice. Exiting..."
        ;;
esac
