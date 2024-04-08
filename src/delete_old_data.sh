#!/bin/bash

# Check if folder path is provided as argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 folder_path"
    exit 1
fi

folder_path=$1

# Check if folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: Folder '$folder_path' does not exist."
    exit 1
fi

# Delete all files in the folder
find "$folder_path" -type f -delete

echo "All files in '$folder_path' have been deleted."
