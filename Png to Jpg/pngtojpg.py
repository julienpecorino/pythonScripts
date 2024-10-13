import os
from PIL import Image

def convert_and_resize_image(file_path, output_path, new_height=2000):
    with Image.open(file_path) as img:
        # Calculate the new width to maintain the aspect ratio
        aspect_ratio = img.width / img.height
        new_width = int(new_height * aspect_ratio)
        
        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save the image in JPG format
        resized_img = resized_img.convert('RGB')  # Ensure no alpha channel for JPG
        resized_img.save(output_path, 'JPEG')

def process_images_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(root, file)
                output_file = os.path.splitext(file)[0] + '.jpg'
                output_path = os.path.join(root, output_file)
                
                convert_and_resize_image(file_path, output_path)
                print(f"Converted and resized: {file_path} to {output_path}")

if __name__ == '__main__':
    main_directory = 'main'
    process_images_in_directory(main_directory)
