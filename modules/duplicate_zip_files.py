import os
import hashlib
import zipfile

def get_file_hash(file_data):
    """Compute the MD5 hash of file data."""
    hasher = hashlib.md5()
    hasher.update(file_data)
    return hasher.hexdigest()

def check_single_zip_for_duplicates(zip_file_path):
    """Check for duplicate files in a single zip archive without opening it.

    Args:
        zip_file_path (str): The path to the zip archive.

    Returns:
        list: A list of duplicate file paths (empty list if no duplicates).

    """
    duplicate_file_paths = []
    file_info_by_size = {}

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            # Skip directories and zero-sized files
            if info.file_size == 0 or info.is_dir():
                continue

            with zip_ref.open(info.filename) as file:
                file_data = file.read()
                file_info = (info.filename, info.file_size, get_file_hash(file_data))

                # Check for duplicate files based on size and hash
                if file_info[1] in file_info_by_size:
                    if file_info[2] in file_info_by_size[file_info[1]]:
                        duplicate_file_paths.append(file_info[0])
                    else:
                        file_info_by_size[file_info[1]].append(file_info[2])
                else:
                    file_info_by_size[file_info[1]] = [file_info[2]]

    return duplicate_file_paths
