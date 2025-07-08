import json
import os

def track_deleted_images(dataset, original_filepaths):
    """
    Detects deleted images by comparing original filepaths with the current dataset,
    deletes the images, and prints the results.
    """
    current_filepaths = {s.filepath for s in dataset}  # Current images in dataset

    # Find deleted images
    deleted_images = list(original_filepaths - current_filepaths)

    if deleted_images:
        # Delete images from the list
        for file_path in deleted_images:
            if isinstance(file_path, str) and file_path.lower().endswith(('.jpg', '.png', '.jpeg')):
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                else:
                    print(f"Skipped (not found): {file_path}")
        print(f"Deleted {len(deleted_images)} images.")
    else:
        print("No images were deleted.")

'''
def delete_images_from_json(json_path):
    # Load JSON file
    with open(json_path, "r") as f:
        data = json.load(f)

    # Define valid image extensions
    valid_extensions = {".jpg", ".png", ".jpeg"}

    # Iterate through paths and delete images
    for file_path in data:
        if isinstance(file_path, str) and file_path.lower().endswith(tuple(valid_extensions)):
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Skipped (not found): {file_path}")

def track_deleted_images(dataset, original_filepaths):
    """
    Detects deleted images by comparing original filepaths with the current dataset.
    Stores deleted file paths in `deleted_images.json`.
    """
    current_filepaths = {s.filepath for s in dataset}  # Current images in dataset

    # Find deleted images
    deleted_images = list(original_filepaths - current_filepaths)

    json_file = "deleted_images.json"
    if deleted_images:
        with open(json_file, "w") as f:
            json.dump(deleted_images, f, indent=4)

        print(f"Deleted {len(deleted_images)} images. File paths stored in 'deleted_images.json'.")
    
    else:
        print("No images were deleted.")

    delete_images_from_json(json_file)
    '''