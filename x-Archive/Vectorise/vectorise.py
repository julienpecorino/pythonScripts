import cv2
import numpy as np
import svgwrite

def bitmap_to_svg(input_image_path, output_svg_path, threshold=128, sigmaX=1, epsilon_factor=0.01, smooth_edges=True):
    # Load the image using OpenCV
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur for initial edge smoothing
    image = cv2.GaussianBlur(image, (3, 3), sigmaX)

    # Apply threshold to binarize the image
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)

    # Find contours from the binary image, including internal contours for holes
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create an SVG file
    dwg = svgwrite.Drawing(output_svg_path, profile='tiny')

    # Process each contour and draw it in the SVG
    for idx, contour in enumerate(contours):
        # Simplify contour to reduce the number of points and smooth the edges
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        simplified_contour = cv2.approxPolyDP(contour, epsilon, True)

        if len(simplified_contour) > 1:
            # Create a path for the contour
            path = svgwrite.path.Path(fill='black', stroke='black', stroke_width="1", fill_rule="evenodd")
            path.push('M', simplified_contour[0][0][0], simplified_contour[0][0][1])  # Move to the first point

            if smooth_edges:
                # Quadratic Bezier curves between points
                for i in range(1, len(simplified_contour)):
                    next_i = (i + 1) % len(simplified_contour)
                    mid_point_x = (simplified_contour[i][0][0] + simplified_contour[next_i][0][0]) / 2
                    mid_point_y = (simplified_contour[i][0][1] + simplified_contour[next_i][0][1]) / 2
                    path.push('Q', simplified_contour[i][0][0], simplified_contour[i][0][1], mid_point_x, mid_point_y)
            else:
                # Straight lines for sharp edges
                for i in range(1, len(simplified_contour)):
                    path.push('L', simplified_contour[i][0][0], simplified_contour[i][0][1])

            path.push('Z')  # Close the path
            dwg.add(path)

    # Save the SVG file
    dwg.save()

# Example usage
input_image_path = 'image.jpg'  # update this to your actual path
output_svg_path = 'image.svg'  # update this to your actual path
bitmap_to_svg(input_image_path, output_svg_path, sigmaX=2, epsilon_factor=0.001, smooth_edges=True)
