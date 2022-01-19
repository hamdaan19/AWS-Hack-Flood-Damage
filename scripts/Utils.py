import numpy as np
from IPython.display import Image, display
from tensorflow import keras
from PIL import ImageOps, Image
from tqdm import tqdm

def display_mask_predictions(output): # takes a numpy array of dimensions: (height, width, num_classes)
    mask = np.argmax(output, axis=-1)
    mask = np.reshape(mask, (240, 320, 1))
    mask = ImageOps.autocontrast(keras.preprocessing.image.array_to_img(mask))
    display(mask)
    
    return mask


def display_mask(output): # takes a numpy array of dimensions: (height, width)
    mask = np.reshape(output, (240, 320, 1))
    mask = ImageOps.autocontrast(keras.preprocessing.image.array_to_img(mask))
    display(mask)
    
    return mask


def get_rgb_segmented(image_array, label, fg_color=[255, 0, 0], bg_color=[0, 0, 0], save_img=False, filename="rgb_img.png"):
    '''
    Utility for converting a prediction array of dimentions (height, width, num_classes)
    into an .png file with one label value color code. 
    '''
    img_arr = np.argmax(image_array, axis=-1)
    img_arr = np.reshape(img_arr, (240, 320))
    img_arr = np.uint8(img_arr)
    
    new_array = np.zeros((240, 320, 3), dtype=int)
    
    for i in tqdm(range(img_arr.shape[0])):
        for j in range(img_arr.shape[1]):
            if img_arr[i][j] == label:
                new_array[i][j] = fg_color
            else: 
                new_array[i][j] = bg_color
    
    new_array = np.uint8(new_array)
    im = Image.fromarray(new_array)
    if save_img == True: im.save(filename)
    
    return im
    