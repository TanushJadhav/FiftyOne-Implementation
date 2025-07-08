# FiftyOne Scripts

This repository contains scripts for managing FiftyOne datasets, including detecting duplicates, checking CVAT annotation status, and computing dataset properties.

### Pre-processing Scripts

#### 1. `read_dataset.py`
Loads a dataset into FiftyOne for viewing.
##### Arguments:
- `--dataset_dir` (str, required): Path to the dataset directory.
- `--name` (str, required): Name of the dataset.
- `--dataset_type` (str, optional, default=`ImageDirectory`): Type of dataset (e.g., ImageDirectoryTree, ImageDirectory, VideoDirectory).
- `--force` (bool, optional): If set, deletes an existing dataset with the same name before loading the new one.

**Note:** If you encounter the error ValueError: Dataset name <name> is not available, you can use the --force option to delete the existing dataset before loading a new one.

**Example:**
```bash
python3 read_dataset.py --dataset_dir <path> --name <dataset_name> --dataset_type ImageDirectoryTree
```

#### 3. `exact_duplicates.py`
Identifies identical duplicate images within a dataset and displays only the duplicates.
##### Arguments:
- `--dataset_dir` (str, required): Path to the dataset directory.
- `--name` (str, required): Name of the dataset.
- `--dataset_type` (str, optional, default=`ImageDirectory`): Type of dataset.

**Example:**
```bash
python3 exact_duplicates.py ---dataset_dir <path> --name <dataset_name> --dataset_type ImageDirectoryTree
```

#### 4. `near_duplicates.py`
Finds images that are either identical or visually similar. A similarity threshold (ranging from 0 to 1) can be set to define the degree of resemblance required.
##### Arguments:
- `--dataset_dir` (str, required): Path to the dataset directory.
- `--name` (str, required): Name of the dataset.
- `--dataset_type` (str, optional, default=`ImageDirectory`): Type of dataset.
- `--threshold` (float, optional, default=`0.02`): Similarity threshold for near duplicates.

**Example:**
```bash
python3 near_duplicates.py --dataset_dir <path> --name <dataset_name> --dataset_type ImageDirectoryTree--threshold 0.02
```

#### 5. `clear_cache.py`
Removes a dataset from FiftyOne's memory.
##### Arguments:
- `dataset_name` (str, required): Name of the dataset to delete.

**Example:**
```bash
python3 clear_cache.py <dataset_name>
```


### CVAT Integration Scripts
When running the script below, you will be prompted to enter your username and password in the command line. Enter them correctly. Afterward, open your CVAT account, and you will find the task created there.

#### 1. `cvat_load_dataset.py`
Loads a dataset into FiftyOne and integrates it with CVAT for annotation, making it ready forf annotations.
##### Arguments:
- `--dataset_dir` (str, required): Path to the dataset directory.
- `--name` (str, required): Name of the dataset.
- `--dataset_type` (str, optional, default=`ImageDirectory`): Type of dataset.
- `--anno_key` (str, required): Annotation key for the CVAT job.
- `--label_field` (str, required): Field to annotate (choices: `detections`, `segmentations`, `keypoints`, `polygons`, `classifications`).
- `--label_type` (str, required): Type of labels (choices: `detections`, `instances`, `polylines`, `keypoints`).
- `--classes` (str, required, space-separated list): List of class names for annotation.

**Example:**
```bash
python3 load_dataset_cvat.py --dataset_dir <path> --name <dataset_name> --dataset_type ImageDirectoryTree --dataset_type ImageDirectory --anno_key <annotation_key> --label_field detections --label_type instances --classes class1 class2 class3
```

#### 2. `cvat_check_status.py`
Loads and combines annotations from CVAT into FiftyOne for review.
#### Arguments:
- `--anno_key` (str, required): Annotation key for the dataset.
- `--name` (str, required): Name of the dataset.

**Example:**
```bash
python3 check_status_cvat.py --anno_key <annotation_key> --name <dataset_name>
```

#### 3. `clear_task.py`
Removes annotation tasks from FiftyOne's memory and, if necessary, deletes the task from CVAT.
##### Arguments:
- `--anno_key` (str, required): Annotation key for the dataset.
- `--name` (str, required): Name of the dataset.
- `--delete_task` (bool, optional, default=`False`): Whether to delete tasks from CVAT.

**Example:**
```bash
python3 finishing_task.py --anno_key <annotation_key> --name <dataset_name> 
```

