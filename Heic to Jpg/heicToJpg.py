import os
from PIL import Image
import pyheif

def convert_heic_to_jpg(input_folder, output_folder):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.heic'):
            # Construct full file path
            heic_file_path = os.path.join(input_folder, filename)
            # Read HEIC file
            heif_file = pyheif.read(heic_file_path)
            # Convert HEIC to JPEG
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            # Define the output file path
            jpg_filename = f"{os.path.splitext(filename)[0]}.jpg"
            jpg_file_path = os.path.join(output_folder, jpg_filename)
            # Save image as JPEG
            image.save(jpg_file_path, "JPEG")
            print(f"Converted {filename} to {jpg_filename}")

if __name__ == "__main__":
    input_folder = 'input'  # Replace with your input folder path
    output_folder = 'output'  # Replace with your output folder path
    convert_heic_to_jpg(input_folder, output_folder)
