import cv2
import os

def capture_screenshots(video_path, num_screenshots=1):
    # Load the video
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video.get(cv2.CAP_PROP_FPS)

    if frame_rate == 0:
        print(f"Error: Could not determine frame rate for video '{video_path}'")
        return

    # Calculate interval for screenshots
    interval = total_frames // (num_screenshots + 1)

    # Capture and save screenshots
    for i in range(1, num_screenshots + 1):
        frame_id = i * interval
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        success, frame = video.read()
        if not success:
            print(f"Error: Could not read frame {frame_id} from video '{video_path}'")
            continue

        # Calculate time in minutes and seconds
        time_in_seconds = frame_id / frame_rate
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)

        # Construct image name with time
        time_str = f"{minutes:02d}_{seconds:02d}"
        screenshot_path = f"{video_path.rsplit('.', 1)[0]}_{i}_{time_str}.jpg"
        cv2.imwrite(screenshot_path, frame)
        print(f"Processing video: {screenshot_path}")

    video.release()

def process_videos_in_folder(folder_path, num_screenshots=1):
    # Initially assume no videos in the root
    videos_in_root = False

    # Check for videos directly in the root directory
    for item in os.listdir(folder_path):
        if item.endswith((".mov", ".mp4")):
            videos_in_root = True
            break

    # If videos are found in the root directory, print the message and stop
    if videos_in_root:
        print("Please tidy up your videos in folder before to continue.")
        return

    # Otherwise, proceed with processing each video found in subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".mov", ".mp4")) and root != folder_path:  # Skip videos in the root directory
                video_path = os.path.join(root, file)
                capture_screenshots(video_path, num_screenshots)

# Folder containing videos
videos_folder = 'videos'  # Update this path to the directory containing your videos

# Process all videos in the videos folder recursively, respecting the new rule
process_videos_in_folder(videos_folder, num_screenshots=100)  # Adjust num_screenshots as needed
