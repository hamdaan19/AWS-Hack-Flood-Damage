import os
from Utils import *
from xception_classification_model import get_xception_model
import numpy as np

PROJECT_DIR = get_project_dir_path()
SPLIT_SIZE = (128, 128)
IN_DIR = os.path.join(PROJECT_DIR, "assets/input_dir")
OUT_DIR = os.path.join(PROJECT_DIR, "assets/output_dir")
MODEL_PATH = os.path.join(PROJECT_DIR, "scripts/archive/Xception_model/Xception_damage_classification.ckpt")

tf.keras.backend.clear_session()
MODEL = get_xception_model()
MODEL.load_weights(MODEL_PATH)

def predict(image, split_size):
    img_arr = np.asarray(image)
    if img_arr.shape[-1] == 4:
        img_arr = img_arr[...,:3]
        
    # Check if (the split) img_arr is of correct size, 
    # else pad the array to the correct size.
    if (img_arr.shape[0] == split_size[0] and img_arr.shape[1] == split_size[1]):
        pass
    else:
        pad_height = split_size[0]-img_arr.shape[0]
        pad_width = split_size[1]-img_arr.shape[1]        
        img_arr = np.pad(img_arr, ((0,pad_height), (0,pad_width), (0,0)), constant_values=0)
        
    img_arr = np.expand_dims(img_arr, axis=0)
    prediction = MODEL.predict(x=img_arr)
    
    return prediction # Returns One-hot encoded vector 

def main(split_size=SPLIT_SIZE):
    IMG_LIST = os.listdir(os.path.join(PROJECT_DIR, "assets/input_dir"))
    print(IMG_LIST)
    
    row_list = []  # 1D list containing nparrays in a row fashion
    main_list = [] # 2D list containing lists (row_list) containing nparrays 
    
    ## Note: This code block takes an image, splits it into smaller images, makes
    ## makes predictions on them and stores it in a 2D array (main_list).
    for img_path in IMG_LIST:
        name, ext = os.path.splitext(img_path)

        split_img_list = split_image(os.path.join(IN_DIR, img_path), split_size=split_size)
        for img_row in tqdm(split_img_list):
            for img in img_row:
                pred_vector = predict(img, split_size=split_size)
                pred_class = np.argmax(pred_vector, axis=1)
                if pred_class == 0:
                    # If damaged, color the block with RED
                    block_arr = np.full(split_size+(3,), [255, 0, 0])
                elif pred_class == 1:
                    # If not damaged, color the block with GREEN
                    block_arr = np.full(split_size+(3,), [0, 255, 0])
                row_list.append(block_arr)
            # Concatenate all arrays in row_list. Note the axis.
            concat_row = np.concatenate((row_list[:]), axis=1)
            row_list = []
            main_list.append(concat_row) 
        # Concatenate all arrays in main_list. Note the axis.
        full_highlighted = np.concatenate((main[:]), axis=0)
        full_highlighted.save(os.path.join(OUT_DIR, f"{name}_highlighted{ext}"))


if __name__ == "__main__":
    main()