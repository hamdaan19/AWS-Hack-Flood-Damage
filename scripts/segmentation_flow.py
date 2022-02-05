import os
from Utils import split_image
import numpy as np
from unet_xception_model import get_model
from Utils import highlight_labels, get_project_dir_path
import tensorflow as tf
from tqdm import tqdm
from PIL import ImageFilter

PROJECT_DIR = get_project_dir_path()

SPLIT_SIZE = (240, 320) # (height, width)
IN_DIR = os.path.join(PROJECT_DIR, "assets/input_dir")
OUT_DIR = os.path.join(PROJECT_DIR, "assets/output_dir")
MODEL_PATH = os.path.join(PROJECT_DIR, "scripts/archive/UNET_X/UNET_X_floodnet.ckpt")

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


def main():
    IMG_LIST = os.listdir(os.path.join(PROJECT_DIR, "assets/input_dir"))

    row_list = []  # 1D list containing nparrays in a row fashion
    main_list = [] # 2D list containing lists (row_list) containing nparrays 
    
    ## Note: This code block takes an image, splits it into smaller images, makes
    ## makes predictions on them and stores it in a 2D array (main_list).
    for n, img_path in enumerate(IMG_LIST): 
        name, ext = os.path.splitext(img_path)
        
        split_img_list = split_image(os.path.join(IN_DIR, img_path), split_size=SPLIT_SIZE)
        print("\nWorking on split-images row by row:")
        for img_row in tqdm(split_img_list):
            for img in img_row:
                pred_arr = predict(img)
                pred_arr = np.squeeze(pred_arr, axis=0)
                row_list.append(pred_arr)
            # Concatenate all arrays in row_list. Note the axis.
            concat_row = np.concatenate((row_list[:]), axis=1)
            row_list = [] # Reseting the list
            main_list.append(concat_row) 
        # Concatenate all arrays in main_list. Note the axis.
        full_mask = np.concatenate((main_list[:]), axis=0)
        highlighted_img = highlight_labels(full_mask, fg_color=[[255, 255, 0], [50, 50, 255]], label=[4, 3])
        # Soften Edges
        highlighted_softened_img = highlighted_img.filter(ImageFilter.ModeFilter(size=10))
        
        # Save the image in the output directory
        highlighted_softened_img.save(os.path.join(OUT_DIR, f"{name}_highlighted{ext}"))
        main_list = []
                

if __name__ == "__main__":
    main()