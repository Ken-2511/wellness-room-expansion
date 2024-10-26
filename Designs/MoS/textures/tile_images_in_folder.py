import os
import cv2
import numpy as np

def modify_output_filename(input_file):
    # Split the input file into directory, base name, and extension
    directory, filename = os.path.split(input_file)
    basename, extension = os.path.splitext(filename)
    
    # Construct the new filename with "tiled" in front
    new_filename = f"tiled_{basename}{extension}"
    
    # Reconstruct the full path if the directory is not empty
    if directory:
        output_file = os.path.join(directory, new_filename)
    else:
        output_file = new_filename
    
    return output_file

def remove_tiled_files(folder_path):
    """
    Removes files that begin with "tiled" in the specified folder.
    
    Parameters:
    - folder_path: Path to the folder where files should be removed.
    """
    for filename in os.listdir(folder_path):
        if filename.startswith("tiled"):
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
                print(f"Removed {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

def tile_images_in_folder(folder_path, output_width, output_height, scale_percent):
    """
    Tiles all PNG, JPEG, and TIF images in the specified folder after removing
    previously tiled images.
    
    Parameters:
    - folder_path: Path to the folder containing the images.
    - output_width: Width of the output images in pixels.
    - output_height: Height of the output images in pixels.
    - scale_percent: Scale of the input images in percentage.
    """
    # First, remove previously tiled images
    remove_tiled_files(folder_path)

    scale_factor = scale_percent / 100

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff")):
            input_file = os.path.join(folder_path, filename)
            print(f"Processing {input_file}...")
            
            img = cv2.imread(input_file, cv2.IMREAD_UNCHANGED)
            if img is None:
                print("Error: Unable to read the image.")
                continue
            
            num_channels = 1 if len(img.shape) == 2 else img.shape[2]
            
            # rotate image
            rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # scale image
            scaled_width = int(img.shape[1] * scale_factor)
            scaled_height = int(img.shape[0] * scale_factor)
            scaled_img = cv2.resize(rotated_img, (scaled_width, scaled_height), interpolation=cv2.INTER_AREA)
            
            num_tiles_x = int(np.ceil(output_width / scaled_width))
            num_tiles_y = int(np.ceil(output_height / scaled_height))
            if num_channels == 1:
                tiled_image = np.tile(scaled_img, (num_tiles_y, num_tiles_x))[:output_height, :output_width]
            else:
                tiled_image = np.tile(scaled_img, (num_tiles_y, num_tiles_x, 1))[:output_height, :output_width, :]
                
            output_file = modify_output_filename(input_file)
            cv2.imwrite(output_file, tiled_image)
            print(f"Output image saved as: {output_file}")

# Example usage:
folder_path = r"wood floor"  # Replace this with the actual path to your folder
output_width = 8420  # Example output width
output_height = 3100  # Example output height
scale_percent = 125  # Example scale percentage

tile_images_in_folder(folder_path, output_width, output_height, scale_percent)
