import os
import shutil

# Assuming the script is run from a directory that contains the 'videos' folder
# Navigate to the 'videos' folder
os.chdir('./videos')

# Get a list of all .mp4 files in the directory
video_files = [f for f in os.listdir() if f.endswith('.mp4')]

# Loop through each video file
for video_file in video_files:
    # Extract the filename without extension
    video_name, _ = os.path.splitext(video_file)

    # Create a folder with the same name as the video file
    os.makedirs(video_name, exist_ok=True)

    # Move the video file into the newly created folder
    shutil.move(video_file, video_name)

    # Inside the newly created folder, create the "Reframed" and "Selection" folders
    os.makedirs(os.path.join(video_name, 'Reframed'), exist_ok=True)
    os.makedirs(os.path.join(video_name, 'Selection'), exist_ok=True)

    print(f"Processing video: {video_name}")

print("All videos processed.")
