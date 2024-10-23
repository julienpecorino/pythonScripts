import subprocess
import sys

def compress_video(input_path, output_path, resolution='2160x3840', scale_factor=1.0):
    """
    Compress and convert a video file to a different format and resolution, with adjustable scaling.

    Args:
    input_path (str): Path to the input video file.
    output_path (str): Path where the output video will be saved.
    resolution (str): Original resolution in WIDTHxHEIGHT format.
    scale_factor (float): Factor to scale the output video resolution (1.0 for original size, 0.5 for half size, etc.).
    """
    try:
        # Extract original width and height from resolution string
        original_width, original_height = map(int, resolution.split('x'))

        # Calculate new width and height based on the scale factor while maintaining aspect ratio
        scaled_width = int(original_width * scale_factor)
        scaled_height = int(original_height * scale_factor)

        # Command to use ffmpeg to convert and compress video with scaling
        command = [
            'ffmpeg',
            '-i', input_path,                    # Input file
            '-vf', f'scale={scaled_width}:{scaled_height}',  # Video filter for scaling
            '-crf', '24',                        # Constant Rate Factor for quality (0-51, where lower is better quality)
            output_path                          # Output file
        ]

        # Execute the command
        subprocess.run(command, check=True)
        print(f"Video has been compressed and converted to {output_path} at resolution {scaled_width}x{scaled_height}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during video processing: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

# Usage example (uncomment and modify the paths as needed):
compress_video('pablo.mov', 'pablo.mp4', resolution='2160x3840', scale_factor=0.15)
