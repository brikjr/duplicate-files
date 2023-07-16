# Duplicate Content Checker

Duplicate Content Checker is a Python script that helps you identify duplicate files within a specified folder and its subdirectories. It calculates the MD5 hash of each file to detect duplicate content and can also calculate duplicate file sizes if required.

## Requirements

- Python 3.6 and above

## Usage

1. Clone or download the repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory containing the `duplicate_content.py` file.

3. Run the following command to check for duplicate files:

   ```shell
   python duplicate_content.py -f <folder_path> [-s]
   
4. Replace <folder_path> with the path to the folder you want to scan for duplicates.

### Optional flag:

-s or --calculate-sizes: Calculate duplicate file sizes as well.
