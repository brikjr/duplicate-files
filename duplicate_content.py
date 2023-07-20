import os
import argparse
import hashlib
import platform
import subprocess
from collections import defaultdict

def get_file_hash(file_path):
    """Calculate the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.

    """
    try:
        if platform.system() == "Darwin":
            # macOS (use md5 command)
            md5_output = subprocess.check_output(["md5", file_path], universal_newlines=True)
            file_hash = md5_output.split()[-1]  # Extract the hash from the output
            return file_hash
        else:
            # Linux/Unix-based systems (use md5sum command)
            md5sum_output = subprocess.check_output(["md5sum", file_path], universal_newlines=True)
            file_hash = md5sum_output.split()[0]  # Extract the hash from the output
            return file_hash
    except subprocess.CalledProcessError as e:
        # Handle any errors that might occur during the md5sum command execution
        print(f"Error calculating hash for {file_path}: {e}")
        return None
    

def check_files_in_folder(folder_path, calculate_file_sizes=False):
    """Check for duplicate files in a folder.

    This function traverses through the specified folder and its subdirectories,
    calculates the MD5 hash of each file, and identifies duplicate files by their hashes.

    Args:
        folder_path (str): The path to the folder.

    """
    # Using collections module defaultdict
    file_hashes = defaultdict(list)
    file_sizes = defaultdict(list)
    
    # Traverse through the folder and its subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = get_file_hash(file_path) # Calculate the hash of the file
            file_hashes[file_hash].append(file_path) # Store the file path with its hash
            
            if calculate_file_sizes:
                file_size = os.path.getsize(file_path)
                file_sizes[file_size].append(file_path)
                
        for subfolder in dirs:
            subfolder_path = os.path.join(root, subfolder)
            check_files_in_folder(subfolder_path, calculate_file_sizes)  # Recursive call to check files in nested folder


    # Iterate over the file hashes and their corresponding file paths
    for file_hash, file_paths in file_hashes.items():
        if len(file_paths) > 1: # Check if there are multiple file paths with the same hash
            print(f"Duplicate files with hash {file_hash}")
            for file_path in file_paths:
                print(file_path) # Print the file paths of the duplicate files
            print()

    if calculate_file_sizes:
        for file_size, file_paths in file_sizes.items():
            if len(file_paths) > 1:
                print(f"Duplicate files with size {file_size} bytes")
                for file_path in file_paths:
                    print(file_path)
                print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check for duplicate files in a folder.')
    parser.add_argument('-f', '--folder', required=True, help='Path to the folder')
    parser.add_argument('-s', '--calculate-sizes', action='store_true', help='Calculate duplicate file sizes')
    args = parser.parse_args()

    folder_path = args.folder
    calculate_sizes = args.calculate_sizes

    check_files_in_folder(folder_path, calculate_sizes)

