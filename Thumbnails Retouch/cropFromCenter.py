import os
from PIL import Image

def crop_and_resize_image(input_path, output_path, size=(512, 512), zoom_factor=5, pan_horizontal=0, pan_vertical=0):
    zoom_scale = 1 + (zoom_factor / 10.0)  # Calculate zoom scale; 1 means no zoom, up to 2
    with Image.open(input_path) as img:
        # Calculate the size to crop to a square based on the zoom scale
        min_dimension = min(img.size) / zoom_scale
        horizontal_padding = (img.size[0] - min_dimension) / 2
        vertical_padding = (img.size[1] - min_dimension) / 2

        # Calculate horizontal and vertical shifts based on pan factors
        max_horizontal_shift = (img.size[0] - min_dimension)
        horizontal_shift = (pan_horizontal / 10.0) * max_horizontal_shift

        max_vertical_shift = (img.size[1] - min_dimension)
        vertical_shift = (pan_vertical / 10.0) * max_vertical_shift

        # Set the crop coordinates ensuring not to go out of image bounds
        left = max(horizontal_padding + horizontal_shift, 0)
        right = min(left + min_dimension, img.size[0])
        top = max(vertical_padding + vertical_shift, 0)
        bottom = min(top + min_dimension, img.size[1])

        # Adjust bounds if out of the image area
        if right > img.size[0]:
            right = img.size[0]
            left = img.size[0] - min_dimension
        if bottom > img.size[1]:
            bottom = img.size[1]
            top = img.size[1] - min_dimension

        # Perform the crop
        img_cropped = img.crop((left, top, right, bottom))

        # Resize the image
        img_resized = img_cropped.resize(size, Image.Resampling.LANCZOS)

        # Save the image
        img_resized.save(output_path, 'JPEG', quality=100)

def process_images_in_folder(main_folder, zoom_factor=5, pan_horizontal=0, pan_vertical=0):
    for root, dirs, files in os.walk(main_folder):
        if 'Selection' in dirs:
            selection_folder = os.path.join(root, 'Selection')
            reframed_folder = os.path.join(root, 'Reframed')
            if not os.path.exists(reframed_folder):
                os.makedirs(reframed_folder)
            else:
                # Remove existing images in the "Reframed" folder before processing new images
                for existing_file in os.listdir(reframed_folder):
                    os.remove(os.path.join(reframed_folder, existing_file))
            for filename in os.listdir(selection_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    input_path = os.path.join(selection_folder, filename)
                    output_path = os.path.join(reframed_folder, filename)
                    crop_and_resize_image(input_path, output_path, zoom_factor=zoom_factor, pan_horizontal=pan_horizontal, pan_vertical=pan_vertical)
                    # Print the name of the processed image
                    print(f"Processed: {filename}")

# Replace 'videos' with the path to your main folder if necessary
process_images_in_folder('videos', zoom_factor=10, pan_horizontal=-1.2, pan_vertical=-2.5)  # Default zoom and pan factors
