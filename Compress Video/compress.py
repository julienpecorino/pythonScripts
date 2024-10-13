import subprocess
import sys

def compress_video(input_path, output_path, resolution='1280x800'):
    """
    Compress and convert a video file to a different format and resolution.

    Args:
    input_path (str): Path to the input video file.
    output_path (str): Path where the output video will be saved.
    resolution (str): Target resolution in WIDTHxHEIGHT format.
    """
    try:
        # Command to use ffmpeg to convert and compress video
        command = [
            'ffmpeg',
            '-i', input_path,             # Input file
            '-vf', f'scale={resolution}', # Video filter for scaling
            '-crf', '24',                 # Constant Rate Factor for quality (0-51, where lower is better quality)
            output_path                   # Output file
        ]

        # Execute the command
        subprocess.run(command, check=True)
        print(f"Video has been compressed and converted to {output_path} at resolution {resolution}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during video processing: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

# Usage example (uncomment and modify the paths as needed):
compress_video('pablo.mov', 'pablo.mp4')
