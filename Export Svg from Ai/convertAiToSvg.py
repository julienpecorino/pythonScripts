import os
import subprocess

# Define input and output directories
input_folder = './input'  # Folder containing your .ai files
output_folder = './output'  # Folder where SVGs will be saved

# Ensure the output directory exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def export_ai_to_svg(input_file):
    """Convert AI file to SVG using Inkscape."""
    output_file = os.path.join(output_folder, os.path.basename(input_file).replace('.ai', '.svg'))

    # Inkscape command for converting AI to SVG
    command = [
        'inkscape',
        '--file', input_file,  # Input AI file
        '--export-plain-svg', output_file  # Output SVG file
    ]

    try:
        # Execute the command
        subprocess.run(command, check=True)
        print(f'Successfully exported {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'Error during exporting {input_file}: {e}')

def process_all_ai_files():
    """Process all AI files in the input folder."""
    for filename in os.listdir(input_folder):
        if filename.endswith('.ai'):
            input_path = os.path.join(input_folder, filename)
            export_ai_to_svg(input_path)

if __name__ == '__main__':
    process_all_ai_files()
