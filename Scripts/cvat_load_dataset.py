#!/usr/bin/env python3

import fiftyone as fo
import argparse
import psycopg2
from psycopg2 import sql

from read_dataset import load_dataset

def connect_to_postgres():
    try:
        # Database connection details
        conn = psycopg2.connect(
            dbname="fiftyone",
            user="postgres",
            password="1234",
            host="localhost",  # or the database host
            port="5432"  # default PostgreSQL port
        )
        print("Connected to PostgreSQL")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
    
def send_event_to_postgres(event_data):
    """
    Inserts a new project task record into the PostgreSQL database.

    Parameters:
        name (str): Name of the individual.
        project_name (str): Name of the project.
        dataset_name (str): Name of the dataset.
        timestamp_start (str): Start timestamp.
        timestamp_end (str): End timestamp.
        task (str): Task description.
        classes (str): Classes associated with the task.
        version (str): Version information.
    """

    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO project_tasks (
            name, project_name, dataset_name, timestamp_start, timestamp_end, task, classes, version
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        );
        """
        cursor.execute(insert_query, event_data)
        conn.commit()
        print(f"Event {event_data[0]} inserted successfully.")
    
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Annotate a FiftyOne dataset using CVAT.")
    parser.add_argument("--name", type=str, required=True, help="Name of the dataset")
    parser.add_argument("--dataset_dir", type=str, required=True, help="Path to the dataset directory")
    parser.add_argument(
        "--dataset_type", type=str, default="ImageDirectory", 
        choices=["ImageDirectory", "VideoDirectory", "ImageDirectoryTree", "VideoDirectoryTree", "yoloDataset"], 
        help="Type of the dataset (default: ImageDirectory)"
    )
    parser.add_argument("--anno_key", type=str, required=True, help="Annotation key for the CVAT job")
    parser.add_argument("--label_field", type=str, required=True, choices=["detections", "segmentations", "keypoints", "polygons", "classifications"], help="Label field to annotate")
    parser.add_argument("--label_type", type=str, required=True, choices=["detections", "instances", "polylines", "keypoints"], help="Type of labels (e.g., instances, detections, polylines, keypoints)")
    parser.add_argument("--classes", type=str, nargs="+", required=True, help="List of class names for annotation (space-separated)")

    args = parser.parse_args()

    # Prompting User Data
    fname = input("Enter your Full Name: ")
    proj_name = input("Enter the name of your Project (eg: HUL, Rhenus): ")
    ds_name = input("Enter name of your dataset/task: ")
    t_start = input("Input Timestamp Start: ")
    t_end = input("Input Timestamp End: ")
    version = input("Enter the Version (\"v1\" if it is the first one): ")

    conn = connect_to_postgres()
    if not conn:
        print("Connection Failed")

    event = (fname, proj_name, ds_name, t_start, t_end, args.label_field, str(args.classes), version)
    send_event_to_postgres(event)

    if conn:
        conn.close()
        print("PostgreSQL connection closed")

    # Load dataset
    dataset = load_dataset(args.dataset_dir, args.name, args.dataset_type)
    dataset.persistent = True

    # Launch the FiftyOne App
    session = fo.launch_app(dataset, address="0.0.0.0")

    # Run the annotation editor
    dataset.annotate(
        anno_key=args.anno_key, 
        label_field=args.label_field,
        label_type=args.label_type,
        classes=args.classes,
        launch_editor=True,
    )
