import unittest
import os
import subprocess

class TestDuplicateFilesCheck(unittest.TestCase):
    def setUp(self):
        # Create a temporary test directory with test files for testing
        self.test_dir = "test_directory"
        os.makedirs(self.test_dir, exist_ok=True)

        # Create some test files with identical content for duplicate testing
        self.file_content = b'This is some test content'
        self.num_files = 5
        for i in range(self.num_files):
            with open(os.path.join(self.test_dir, f"test_file_{i}.txt"), "wb") as f:
                f.write(self.file_content)

        # Create a test file with different content for uniqueness testing
        with open(os.path.join(self.test_dir, "unique_file.txt"), "wb") as f:
            f.write(b'This file is unique')

    def tearDown(self):
        # Clean up the test directory and files
        for root, _, files in os.walk(self.test_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            os.rmdir(root)

    def test_duplicate_files_check(self):
        # Get the absolute path to the main script file
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "duplicate_content.py"))
        
        # Run the main script in a subprocess to avoid interference
        folder_path = os.path.abspath(self.test_dir)
        cmd = f"python {script_path} -f {folder_path} -s"
        result = subprocess.check_output(cmd, shell=True, universal_newlines=True)


        # Print the script's output for debugging
        print(result)

        # Split the result into lines to check for duplicates
        lines = result.strip().split("\n")
        duplicate_lines = [line for line in lines if line.startswith("Duplicate files with")]

        # Assert that the script found the correct number of duplicates
        self.assertEqual(len(duplicate_lines), 1)

        # Assert that the script output contains the expected number of lines
        self.assertEqual(len(lines), 11)  # Updated assertion to expect 11 lines in total

if __name__ == "__main__":
    unittest.main()
