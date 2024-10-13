import cv2
import numpy as np
import svgwrite

def bitmap_to_svg(input_image_path, output_svg_path, threshold=128, sigmaX=2):
    # Load the image using OpenCV
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur for smoothing edges; larger kernel size might be more effective
    image = cv2.GaussianBlur(image, (5, 5), sigmaX)

    # Apply threshold to binarize the image
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)

    # Find contours from the binary image including internal contours for holes
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Create an SVG file
    dwg = svgwrite.Drawing(output_svg_path, profile='tiny')

    # Process each contour and draw it in the SVG
    for idx, contour in enumerate(contours):
        # Simplify contour to reduce the number of points
        epsilon = 0.0025 * cv2.arcLength(contour, True)
        simplified_contour = cv2.approxPolyDP(contour, epsilon, True)

        # Convert contour coordinates to a list of tuples ensuring they are properly formatted
        points = [(int(x), int(y)) for x, y in simplified_contour.squeeze()]

        if len(points) > 1:
            # Check if this contour is a hole (child contour)
            if hierarchy[0][idx][3] != -1:  # if it has a parent
                fill_color = 'white'  # holes should be white
            else:
                fill_color = 'black'  # outer contours should be black

            # Add polygons to SVG filled appropriately, no stroke
            dwg.add(dwg.polygon(points, fill=fill_color, stroke='none'))

    # Save the SVG file
    dwg.save()

# Example usage
input_image_path = 'image.jpg'  # update this to your actual path
output_svg_path = 'image.svg'  # update this to your actual path
bitmap_to_svg(input_image_path, output_svg_path, sigmaX=2)
