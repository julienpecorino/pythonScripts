import os
from PIL import Image

def compress_image(input_folder, output_folder, quality=85, max_width=None):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Construct full file path
            file_path = os.path.join(input_folder, filename)
            # Open the image file
            with Image.open(file_path) as img:
                # Resize the image if max_width is specified
                if max_width:
                    aspect_ratio = img.height / img.width
                    new_height = int(max_width * aspect_ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Define the output file path
                output_file_path = os.path.join(output_folder, filename)
                
                # Save the compressed image
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    img.save(output_file_path, "JPEG", quality=quality, optimize=True)
                elif filename.lower().endswith('.png'):
                    img.save(output_file_path, "PNG", optimize=True)
                
                print(f"Compressed and saved {filename} to {output_file_path}")

if __name__ == "__main__":
    input_folder = 'input'  # Replace with your input folder path
    output_folder = 'output'  # Replace with your output folder path
    quality = 85  # Set the desired quality level (1-100) for JPEG compression
    max_width = 2000  # Set the maximum width for resizing (None for no resizing)
    
    compress_image(input_folder, output_folder, quality, max_width)

