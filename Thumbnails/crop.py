import cv2
import numpy as np
import os
import fnmatch
from PIL import Image

def find_subjects_bounds(image, threshold_value=200, roi_margin=50):
    roi_x_min = roi_margin
    roi_y_min = roi_margin
    roi_x_max = image.shape[1] - roi_margin
    roi_y_max = image.shape[0] - roi_margin
    roi = image[roi_y_min:roi_y_max, roi_x_min:roi_x_max]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    if not contours:
        return 0, 0, image.shape[1], image.shape[0]
    x_min = min([cv2.boundingRect(contour)[0] for contour in contours])
    y_min = min([cv2.boundingRect(contour)[1] for contour in contours])
    x_max = max([cv2.boundingRect(contour)[0] + cv2.boundingRect(contour)[2] for contour in contours])
    y_max = max([cv2.boundingRect(contour)[1] + cv2.boundingRect(contour)[3] for contour in contours])
    x_min_global = x_min + roi_x_min
    y_min_global = y_min + roi_y_min
    x_max_global = x_max + roi_x_min
    y_max_global = y_max + roi_y_min
    return x_min_global, y_min_global, x_max_global, y_max_global

def resize_with_aspect_ratio(image, target_size):
    image_ratio = image.width / image.height
    target_ratio = target_size[0] / target_size[1]

    if image_ratio > target_ratio:
        # The image is wider than required: resize by width
        resized_width = target_size[0]
        resized_height = round(target_size[0] / image_ratio)
    else:
        # The image is taller than required: resize by height
        resized_height = target_size[1]
        resized_width = round(target_size[1] * image_ratio)

    image = image.resize((resized_width, resized_height), Image.LANCZOS)

    # Create new image with white background and paste the resized image onto it
    new_image = Image.new('RGB', target_size, (255, 255, 255))
    offset_x = (target_size[0] - resized_width) // 2
    offset_y = (target_size[1] - resized_height) // 2
    new_image.paste(image, (offset_x, offset_y))
    return new_image

def adjust_bbox_to_aspect_ratio(x1, y1, x2, y2, output_aspect_ratio, padding=0):
    bbox_width = x2 - x1
    bbox_height = y2 - y1
    bbox_aspect_ratio = bbox_width / bbox_height
    center_x = x1 + bbox_width / 2
    center_y = y1 + bbox_height / 2
    if bbox_aspect_ratio < output_aspect_ratio:
        new_width = bbox_height * output_aspect_ratio
        x1 = max(0, center_x - new_width / 2)
        x2 = x1 + new_width
    elif bbox_aspect_ratio > output_aspect_ratio:
        new_height = bbox_width / output_aspect_ratio
        y1 = max(0, center_y - new_height / 2)
        y2 = y1 + new_height
    padding_x = padding
    padding_y = padding
    if (x2 - x1) / (y2 - y1) < output_aspect_ratio:
        padding_x = padding * output_aspect_ratio / ((x2 - x1) / (y2 - y1))
    elif (x2 - x1) / (y2 - y1) > output_aspect_ratio:
        padding_y = padding * ((x2 - x1) / (y2 - y1)) / output_aspect_ratio
    x1 -= padding_x
    x2 += padding_x
    y1 -= padding_y
    y2 += padding_y
    return int(x1), int(y1), int(x2), int(y2)

def process_images(base_dir, output_size=(512, 512), padding=50, threshold_value=200):
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        for subfolder in os.listdir(folder_path):
            if fnmatch.fnmatch(subfolder, 'Selection*'):
                input_dir = os.path.join(folder_path, subfolder)
                output_dir = os.path.join(folder_path, 'Reframed')
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                files = os.listdir(input_dir)
                total_files = len(files)
                print(f"Total files to process in {folder}/{subfolder}: {total_files}")
                for idx, filename in enumerate(files):
                    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        continue
                    print(f"Processing {idx + 1}/{total_files}: {filename}")
                    full_path = os.path.join(input_dir, filename)
                    image = cv2.imread(full_path)
                    if image is None:
                        print(f"Skipping {filename}: Failed to load.")
                        continue
                    x1, y1, x2, y2 = find_subjects_bounds(image, threshold_value=threshold_value)
                    output_aspect_ratio = output_size[0] / output_size[1]
                    x1, y1, x2, y2 = adjust_bbox_to_aspect_ratio(x1, y1, x2, y2, output_aspect_ratio, padding=padding)
                    crop_img = image[y1:y2, x1:x2]
                    if crop_img.size == 0 or crop_img.shape[0] == 0 or crop_img.shape[1] == 0:
                        print(f"Skipping {filename}: Crop is empty or invalid.")
                        continue
                    pil_img = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
                    final_img = resize_with_aspect_ratio(pil_img, output_size)
                    output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')
                    final_img.save(output_file_path)

base_directory = 'videos'
process_images(base_directory)
