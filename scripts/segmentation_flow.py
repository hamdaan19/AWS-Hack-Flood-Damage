import os
from tkinter import Image
from Utils import split_image
import numpy as np
from unet_xception_model import get_model
from Utils import highlight_labels, get_project_dir_path
import tensorflow as tf
from tqdm import tqdm
from PIL import ImageFilter
import PIL

PROJECT_DIR = get_project_dir_path()

SPLIT_SIZE = (240, 320) # (height, width)
IN_DIR = os.path.join(PROJECT_DIR, "assets/input_dir")
OUT_DIR = os.path.join(PROJECT_DIR, "assets/output_dir")
MODEL_PATH = os.path.join(PROJECT_DIR, "models/UNET_X/UNET_X_floodnet.ckpt")

tf.keras.backend.clear_session()
MODEL = get_model(img_size=SPLIT_SIZE, in_channels=3, classes=10)
MODEL.load_weights(MODEL_PATH)

def predict(image):
    img_arr = np.array(image)
    if img_arr.shape[-1] == 4:
        img_arr = img_arr[...,:3]
    # Check if (the split) img_arr is of correct size, 
    # else pad the array to the correct size.
    if (img_arr.shape[0] == SPLIT_SIZE[0] and img_arr.shape[1] == SPLIT_SIZE[1]):
        pass
    else:
        pad_height = SPLIT_SIZE[0]-img_arr.shape[0]
        pad_width = SPLIT_SIZE[1]-img_arr.shape[1]        
        img_arr = np.pad(img_arr, ((0,pad_height), (0,pad_width), (0,0)), constant_values=0)
    
    img_arr = np.expand_dims(img_arr, axis=0)
    prediction = MODEL.predict(x=img_arr)
    
    return prediction # Returns nparray of size (1, height, width, channels #10 )

def get_progress_bar_increment(img_path, R, C):
    time_p = 8.00 * 1e-6
    time_i = 0.1302 

    total_blocks = R*C 
    img = PIL.Image.open(img_path)
    img_W, img_H = img.size
    new_img_H = SPLIT_SIZE[0] * (img_H//SPLIT_SIZE[0]+1) if img_H%SPLIT_SIZE[0] != 0 else img_H
    new_img_W = SPLIT_SIZE[1] * (img_H//SPLIT_SIZE[1]+1) if img_H%SPLIT_SIZE[1] != 0 else img_W

    total_pixels = new_img_H * new_img_W
    
    total_time = (total_blocks*time_i) + (total_pixels*time_p)
    print("Time: ", total_time, total_pixels, total_pixels*time_p, total_blocks*time_i)
    percentage_increment = time_i/total_time * 100

    return percentage_increment

def main(gui_root=None, bar=None, txt=None):
    IMG_LIST = os.listdir(os.path.join(PROJECT_DIR, "assets/input_dir"))

    row_list = []  # 1D list containing nparrays in a row fashion
    main_list = [] # 2D list containing lists (row_list) containing nparrays 
    
    ## Note: This code block takes an image, splits it into smaller images, makes
    ## makes predictions on them and stores it in a 2D array (main_list).
    for n, img_path in enumerate(IMG_LIST): 
        name, ext = os.path.splitext(img_path)
        current_img_path = os.path.join(IN_DIR, img_path)
        split_img_list = split_image(current_img_path, split_size=SPLIT_SIZE)

        nRows = len(split_img_list)
        nCols = len(split_img_list[0])
        increment_val = get_progress_bar_increment(current_img_path, nRows, nCols)
        print(increment_val)

        print("\nWorking on split-images row by row:")
        for img_row in tqdm(split_img_list):
            for img in img_row:
                pred_arr = predict(img)
                pred_arr = np.squeeze(pred_arr, axis=0)
                row_list.append(pred_arr)
                if gui_root != None:
                    bar['value'] += increment_val
                    txt.config(text=f"{round(bar['value'], 1)}%")
                    gui_root.update()
            # Concatenate all arrays in row_list. Note the axis.
            concat_row = np.concatenate((row_list[:]), axis=1)
            row_list = [] # Reseting the list
            main_list.append(concat_row) 
        # Concatenate all arrays in main_list. Note the axis.
        full_mask = np.concatenate((main_list[:]), axis=0)
        highlighted_img = highlight_labels(full_mask, fg_color=[[255, 255, 0], [50, 50, 255]], label=[4, 3], gui_root=gui_root, bar=bar, txt=txt)
        # Soften Edges
        highlighted_softened_img = highlighted_img.filter(ImageFilter.ModeFilter(size=10))
        
        # Save the image in the output directory
        highlighted_softened_img.save(os.path.join(OUT_DIR, f"{name}_highlighted{ext}"))
        main_list = []
                

if __name__ == "__main__":
    main()