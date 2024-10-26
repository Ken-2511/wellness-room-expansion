import numpy as np
import cv2

def resize_image(image: np.ndarray, factor: int) -> np.ndarray:
    """
    Resizes an image by taking the average value of the pixels in each block of size factor x factor.
    
    Parameters:
    - f_name: np.ndarray, the input image as a NumPy array.
    - factor: int, the size of the block over which to calculate the average pixel value.
    
    Returns:
    - np.ndarray: The resized image as a NumPy array.
    """
    # Calculate the new dimensions
    new_height = image.shape[0] // factor
    new_width = image.shape[1] // factor
    
    # Initialize an empty array for the resized image
    resized_image = np.zeros((new_height, new_width, image.shape[2]), dtype=np.uint8)
    
    # Iterate over each block of the image and calculate the average color
    for i in range(new_height):
        for j in range(new_width):
            # Calculate the start and end indices of the current block
            start_i, end_i = i * factor, (i + 1) * factor
            start_j, end_j = j * factor, (j + 1) * factor
            
            # Extract the block and calculate its average color
            block = image[start_i:end_i, start_j:end_j]
            average_color = block.mean(axis=(0, 1))
            
            # Assign the average color to the corresponding position in the resized image
            resized_image[i, j] = average_color
    
    return resized_image

import numpy as np
import cv2
import sys

def replace_color_with_red(image_path, target_colors, threshold=30):
    """
    Replace pixels similar to a specified color with red in the given image.

    Parameters:
    - image_path: path to the input image.
    - target_color: a tuple (R, G, B) specifying the color to match.
    - threshold: maximum distance between colors to consider a pixel similar.

    Returns:
    - num_similar_pixels: Number of pixels similar to the specified color.
    - total_pixels: Total number of pixels in the image.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found")
        sys.exit()

    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize a mask to keep track of matched pixels
    overall_mask = np.zeros(image_rgb.shape[:2], dtype=bool)

    for target_color in target_colors:
        # Calculate the distance between each pixel and the current target color
        distance = np.sqrt(np.sum((image_rgb - np.array(target_color))**2, axis=2))
        
        # Update mask for pixels within the threshold for the current color
        mask = distance < threshold
        overall_mask |= mask

    # Count similar pixels
    num_similar_pixels = np.sum(overall_mask)

    # Replace similar pixels with red
    image_rgb[overall_mask] = [255, 0, 0]  # RGB for red

    # Convert back to BGR for saving/displaying with OpenCV
    result_image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # Optionally, save or display the result image
    cv2.imwrite('result_image.png', result_image)
    # cv2.imshow('Result', result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    total_pixels = image.shape[0] * image.shape[1]

    return num_similar_pixels, total_pixels


# Example usage
temp = [(.149, .364, .141), (.364, .423, .262), (.251, .427, .243)]
# 4
temp = [(.219, .258, .125), (.349, .380, .387), (.078, .215, .074)]
# 5
temp = [(.09, .254, .054), (.168, .392, .204), (.216, .376, .296)]
#6
temp = [(.278, .572, .329), (.231, .467, .134), (.329, .419, .239)]

target_colours = []
for colour in temp:
    target_colours.append([])
    for i, c in enumerate(colour):
        target_colours[-1].append(c * 255)


image = cv2.imread("ratio6.png", cv2.IMREAD_UNCHANGED)
image = resize_image(image, 5)
cv2.imwrite("ratio6_changed.png", image)

threshold = 30
num_similar, total = replace_color_with_red('ratio6_changed.png', target_colours, threshold)
print(f"Similar pixels: {num_similar}, Total pixels: {total}")
print(f"Green ratio: {num_similar / total:.4f}")
