from PIL import Image, ImageDraw
import numpy as np
import os

def interpolate_color(start_color, end_color, factor):
    """Interpolate between two colors by a factor between 0 and 1."""
    return tuple([
        int(start_color[i] + (end_color[i] - start_color[i]) * factor)
        for i in range(3)
    ])

def replace_white_bands_with_gradient(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to RGB if it is not
        img = img.convert("RGB")

        # Load pixels
        pixels = img.load()

        # Get the size of the image
        width, height = img.size

        # Determine the height of the top white band
        top_band_height = 0
        for y in range(height):
            if all(pixels[x, y] == (255, 255, 255) for x in range(width)):
                top_band_height += 1
            else:
                break

        # Determine the height of the bottom white band
        bottom_band_height = 0
        for y in range(height - 1, -1, -1):
            if all(pixels[x, y] == (255, 255, 255) for x in range(width)):
                bottom_band_height += 1
            else:
                break

        # If there is no top or bottom white band, return
        if top_band_height == 0 and bottom_band_height == 0:
            return None

        # Create a new image for the gradient
        gradient_img_top = Image.new('RGB', (width, top_band_height))
        gradient_img_bottom = Image.new('RGB', (width, bottom_band_height))
        draw_top = ImageDraw.Draw(gradient_img_top)
        draw_bottom = ImageDraw.Draw(gradient_img_bottom)

        # Get 50 evenly spaced color samples for top and bottom bands
        sample_points = np.linspace(0, width - 1, 12, dtype=int)
        colors_top = [pixels[x, top_band_height] for x in sample_points]
        colors_bottom = [pixels[x, height - bottom_band_height - 1] for x in sample_points]

        # Draw the smooth gradient for top band
        if top_band_height > 0:
            for x in range(width):
                # Find the two closest sample points
                right_sample_index = np.searchsorted(sample_points, x, side='right')
                left_sample_index = max(0, right_sample_index - 1)

                # Calculate interpolation factor
                if right_sample_index < len(sample_points):
                    span = sample_points[right_sample_index] - sample_points[left_sample_index]
                    factor = (x - sample_points[left_sample_index]) / span if span else 0
                    color = interpolate_color(colors_top[left_sample_index], colors_top[right_sample_index], factor)
                else:
                    color = colors_top[-1]

                # Draw the interpolated color
                draw_top.line([(x, 0), (x, top_band_height)], fill=color)

        # Draw the smooth gradient for bottom band
        if bottom_band_height > 0:
            for x in range(width):
                # Find the two closest sample points
                right_sample_index = np.searchsorted(sample_points, x, side='right')
                left_sample_index = max(0, right_sample_index - 1)

                # Calculate interpolation factor
                if right_sample_index < len(sample_points):
                    span = sample_points[right_sample_index] - sample_points[left_sample_index]
                    factor = (x - sample_points[left_sample_index]) / span if span else 0
                    color = interpolate_color(colors_bottom[left_sample_index], colors_bottom[right_sample_index], factor)
                else:
                    color = colors_bottom[-1]

                # Draw the interpolated color
                draw_bottom.line([(x, 0), (x, bottom_band_height)], fill=color)

        # Blend the gradient with the original image for top band
        for y in range(top_band_height):
            for x in range(width):
                gradient_color_top = gradient_img_top.getpixel((x, y))
                pixels[x, y] = gradient_color_top

        # Blend the gradient with the original image for bottom band
        for y in range(height - bottom_band_height, height):
            for x in range(width):
                gradient_color_bottom = gradient_img_bottom.getpixel((x, y - (height - bottom_band_height)))
                pixels[x, y] = gradient_color_bottom

        # Overwrite the original image with the corrected one
        img.save(image_path)

        return image_path  # Return the same image path

def process_images_in_folder(folder_path):
    """Process images within the given folder."""
    # Iterate over files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # If the file is a directory, recursively process it
        if os.path.isdir(file_path):
            process_images_in_folder(file_path)
        else:
            # Process only image files
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                corrected_image_path = replace_white_bands_with_gradient(file_path)
                if corrected_image_path:
                    print(f"The original image {file_path} has been replaced with the corrected one.")

def process_videos_folder(videos_folder):
    """Process the 'Reframed' folders within the 'videos' folder."""
    for root, dirs, files in os.walk(videos_folder):
        for dir_name in dirs:
            if dir_name.lower() == 'reframed':
                reframed_folder_path = os.path.join(root, dir_name)
                process_images_in_folder(reframed_folder_path)

# Call the processing function directly
videos_folder = 'videos'  # Update this with your main folder path
process_videos_folder(videos_folder)
