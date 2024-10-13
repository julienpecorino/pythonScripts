from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import os

def adjust_contrast(image, level):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(level)

def adjust_exposure(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_gamma(image, gamma):
    gamma_table = [((i / 255.0) ** (1.0 / gamma)) * 255 for i in range(256)]
    gamma_table = np.array(gamma_table, dtype='uint8')
    if image.mode == 'RGB':
        gamma_table = np.tile(gamma_table, [3, 1]).flatten()
    return Image.fromarray(np.array(image).astype('uint8')).point(gamma_table)

def adjust_saturation(image, level):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(level)

def adjust_blacks(image, level):
    lut = np.array([i * level if i < 128 else i for i in range(256)])
    if image.mode == 'RGB':
        lut = np.tile(lut, 3)
    return image.point(lut.tolist())

def adjust_lights(image, level):
    lut = np.array([i if i < 128 else i * level for i in range(256)])
    if image.mode == 'RGB':
        lut = np.tile(lut, 3)
    return image.point(lut.tolist())

def process_images_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if "Reframed" in dirs:
            ref_folder = os.path.join(root, "Reframed")
            for image_name in os.listdir(ref_folder):
                if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                    image_path = os.path.join(ref_folder, image_name)
                    image = Image.open(image_path)

                    # Adjust image attributes
                    image = adjust_contrast(image, 1)
                    image = adjust_exposure(image, 1)
                    image = adjust_gamma(image, 1.1)
                    image = adjust_saturation(image, 1)
                    image = adjust_blacks(image, 1)
                    image = adjust_lights(image, 1)

                    # Save the modified image, replacing the original
                    image.save(image_path)

# Define your main folder
main_folder = 'videos'
process_images_in_folder(main_folder)
