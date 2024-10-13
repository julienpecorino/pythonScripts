import os

def rename_subfolders(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for dir_name in dirs:
            if "Exercises" in dir_name or "Selection" in dir_name or "Exercise" in dir_name:
                # Construct the full path to the current directory and the new name
                current_dir_path = os.path.join(root, dir_name)
                new_dir_path = os.path.join(root, "Selection")

                # If the directory has already been renamed or another "Selection" exists, we skip
                if dir_name == "Selection" or os.path.exists(new_dir_path):
                    continue

                # Rename the directory
                os.rename(current_dir_path, new_dir_path)
                print(f'Renamed "{dir_name}" to "Selection"')

# Replace 'path_to_videos_folder' with the actual path to the 'videos' folder
path_to_videos_folder = 'videos'
rename_subfolders(path_to_videos_folder)
