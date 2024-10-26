import cv2
import numpy as np
import os

def get_mean(f_name):
    img = cv2.imread(f_name, cv2.IMREAD_UNCHANGED).reshape(-1, 4)

    image = np.zeros_like(img, dtype="float32")

    num_pixels = np.sum(img[:, -1] > 127)

    image[:] = img / 255

    factor = np.array([.299, .587, .114, 0])

    temp = np.sum(image * factor)

    average_value = temp / num_pixels
    print(num_pixels, image.shape)

    print(f"File name: {f_name}, mean greyscale value is {average_value:.4f}")

    return average_value

def get_max(f_name):
    img = cv2.imread(f_name)

    image = np.zeros_like(img, dtype="float32")

    image[:] = img / 255

    factor = np.array([.299, .587, .114])

    temp = np.sum(image * factor, axis=-1)

    print(f"File name: {f_name}, brightest greyscale value is {temp.max():.4f}")

    return temp.max()

def interpolate_lux(greyscale):
    # Data points sorted by greyscale value, including (0, 0)
    data_points = [
        (0, 0), (0.1333, 10), (0.2235, 25), (0.3165, 50), (0.4392, 100),
        (0.5294, 150), (0.6039, 200), (0.6706, 250), (0.7529, 325),
        (0.8275, 400), (0.9137, 500)
    ]
    
    # Handle cases outside the known range
    if greyscale <= data_points[0][0]:
        return data_points[0][1]
    if greyscale >= data_points[-1][0]:
        return data_points[-1][1]
    
    # Find the two nearest points
    for i in range(len(data_points) - 1):
        if data_points[i][0] <= greyscale <= data_points[i + 1][0]:
            x1, y1 = data_points[i]
            x2, y2 = data_points[i + 1]
            break
    
    # Linear interpolation
    return y1 + (y2 - y1) * (greyscale - x1) / (x2 - x1)

'''
folder_name = "light intensity"
for f_name in os.listdir(folder_name):
    # f_name = "cube.png"

    #get_mean(f_name)
    get_max(os.path.join(folder_name, f_name))
'''
value = get_mean("light intensity/probe.png")
print(interpolate_lux(value))
