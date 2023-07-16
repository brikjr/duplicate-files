import os
import argparse
import hashlib
from collections import defaultdict

def get_file_hash(file_path):
    """Calculate the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.

    """
    
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        file_content = f.read() # Read the entire file content
        hash_md5.update(file_content) # Update the hash with the file content
    return hash_md5.hexdigest() # Return the hexadecimal representation of the hash
    

def check_files_in_folder(folder_path):
    """Check for duplicate files in a folder.

    This function traverses through the specified folder and its subdirectories,
    calculates the MD5 hash of each file, and identifies duplicate files by their hashes.

    Args:
        folder_path (str): The path to the folder.

    """
    file_hashes = defaultdict(list)

    # Traverse through the folder and its subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = get_file_hash(file_path) # Calculate the hash of the file
            file_hashes[file_hash].append(file_path) # Store the file path with its hash

    # Iterate over the file hashes and their corresponding file paths
    for file_hash, file_paths in file_hashes.items():
        if len(file_paths) > 1: # Check if there are multiple file paths with the same hash
            print(f"Duplicate files with hash {file_hash}")
            for file_path in file_paths:
                print(file_path) # Print the file paths of the duplicate files
            print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check for duplicate files in a folder.')
    parser.add_argument('-f', '--folder', required=True, help='Path to the folder')
    args = parser.parse_args()

    folder_path = args.folder
    check_files_in_folder(folder_path)
