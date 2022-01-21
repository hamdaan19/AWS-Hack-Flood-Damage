import numpy as np
from IPython.display import Image, display
from tensorflow import keras
from PIL import ImageOps, Image
from tqdm import tqdm
import os

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


def highlight_labels(image_array, label, fg_color=[255, 255, 0], bg_color=[0, 0, 0], save_img=False, filename="rgb_img.png"):
    '''
    Utility for converting a prediction array of dimentions (height, width, num_classes)
    into an .png file with one label value color code. Initial name was get_rgb_segmented() 
    '''
    img_arr = np.argmax(image_array, axis=-1) # (h, w, classes) -> (h, w)
    img_arr = np.uint8(img_arr)
    
    h = img_arr.shape[0]
    w = img_arr.shape[1]
    
    new_array = np.zeros((h, w, 3), dtype=int)
    
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
    
def split_image(path, split_size=(240, 320), save=False): # split_size=(height, width)
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    
    img = Image.open(path)
    width, height = img.size
    
    out_list = []
    row_list = []
    i = 0
    j = 0
    
    for i, yi in enumerate(range(0, height, split_size[0])):
        for j, xi in enumerate(range(0, width, split_size[1])):
            box = (
                xi,
                yi,
                xi+split_size[1] if xi+split_size[1] < width else width-1,
                yi+split_size[0] if yi+split_size[0] < height else height-1,
            )
            current_img = img.crop(box)
            row_list.append(current_img)
            if save == True:
                out_path = os.path.join("../assets/output_dir", f"{name}_{i}_{j}{ext}")
                current_img.save(out_path)
            
        out_list.append(row_list)
        row_list = [] # Empytying the list
        
    return out_list