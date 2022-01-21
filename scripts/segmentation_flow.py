import os
from Utils import split_image
import numpy as np
from unet_xception_model import get_model

IMG_LIST = os.listdir("../assets/input_dir")
SPLIT_SIZE = (240, 320) # (height, width)
OUT_DIR = "../assets/output_dir"
MODEL_PATH = "archive/UNET_X/UNET_X_floodnet.ckpt"

def load_model():
    model = get_model(img_size=SPLIT_SIZE, in_channels=3, classes=10)
    model.load_weights(MODEL_PATH)
    return model

def predict(image):
    img_arr = np.array(image)
    # Check if (the split) img_arr is of correct size, 
    # else pad the array to the correct size.
    if (img_arr.shape[0] == SPLIT_SIZE[0] and img_arr.shape[1] == SPLIT_SIZE[1]):
        pass
    else:
        pad_height = SPLIT_SIZE[0]-img_arr.shape[0]
        pad_width = SPLIT_SIZE[1]-img_arr.shape[1]        
        img_arr = np.pad(img_arr, ((0,pad_height), (0,pad_width), (0,0)), constant_values=0)
    
    img_arr = np.expand_dims(img_arr, axis=0)
    model = load_model()
    prediction = model.predict(x=img_arr)
    
    return prediction # Returns nparray of size (1, height, width, channels #10 )


def main():
    row_list = []  # 1D list containing nparrays in a row fashion
    main_list = [] # 2D list containing lists (row_list) containing nparrays 
    
    ## Note: This code block takes an image, splits it into smaller images, makes
    ## makes predictions on them and stores it in a 2D array (main_list).
    for n, img_path in enumerate(IMG_LIST): 
        name, ext = os.path.splitext(img_path)
        
        split_img_list = split_image(img_path, split_size=SPLIT_SIZE)
        for img_row in split_img_list:
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
        highlighted_img = highlight_labels(full_mask, label=4)
        
        # Save the image in the output directory
        highlighted_img.save(os.path.join(OUT_DIR, f"{name}_{n}{ext}"))
                

if __name__ == "__main__":
    main()