import os
import shutil
import glob

# Set the path to the "videos" directory. Assuming it's relative to the current working directory.
videos_path = "./videos"

# Navigate to the "videos" directory
os.chdir(videos_path)

# Get a list of all directories one level deep within "/videos"
directories = [d for d in os.listdir('.') if os.path.isdir(d)]

# Loop through each directory
for directory in directories:
    # Construct the path to each directory
    dir_path = os.path.join('.', directory)

    # Rename "Reframed" to "Thumbnails" before any deletion
    reframed_path = os.path.join(dir_path, 'Reframed')
    thumbnails_path = os.path.join(dir_path, 'Thumbnails')
    if os.path.exists(reframed_path):
        os.rename(reframed_path, thumbnails_path)
        print(f"Renamed '{reframed_path}' to '{thumbnails_path}'")

    # Find all .jpg files within the directory, excluding the "Thumbnails" subdirectories
    jpg_files = [f for f in glob.glob(os.path.join(dir_path, '**', '*.jpg'), recursive=True)
                 if "Thumbnails" not in f]

    # Find all video files within the directory, excluding the "Thumbnails" subdirectories
    video_files = [f for f in glob.glob(os.path.join(dir_path, '**', '*.mp4'), recursive=True) +
                   glob.glob(os.path.join(dir_path, '**', '*.avi'), recursive=True) +
                   glob.glob(os.path.join(dir_path, '**', '*.mov'), recursive=True)
                   if "Thumbnails" not in f]

    # Delete the found .jpg files
    for file_path in jpg_files:
        os.remove(file_path)
        print(f"Deleted: {file_path}")

    # Delete the found video files
    for file_path in video_files:
        os.remove(file_path)
        print(f"Deleted: {file_path}")

    # Construct the path to the "Selection" folder and delete
    selection_path = os.path.join(dir_path, 'Selection')
    if os.path.exists(selection_path):
        shutil.rmtree(selection_path)
        print(f"Deleted folder: {selection_path}")

# Note: The script prints the paths of deleted files and directories, and renamed directories.
# Remove the print statements if no output is desired.
