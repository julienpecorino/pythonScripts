import os

def count_files_in_thumbnails(root_dir):
    total_files = 0
    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the last part of the path is 'Thumbnails'
        if 'Thumbnails' == os.path.basename(dirpath):
            # Add the count of files in this directory to the total count
            total_files += len(filenames)

    return total_files

# Set the root directory where to start counting
root_directory = 'videos'
# Count the files
file_count = count_files_in_thumbnails(root_directory)
# Output the result
print(f"Total number of files in 'Thumbnails' folders: {file_count}")
