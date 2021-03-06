from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import os, io, sys
import shutil
import tkinter as tk

CURRENT_DIR = os.getcwd()
sys.path.insert(1, os.path.join(CURRENT_DIR, ".."))
import segmentation_flow
import classification_flow
from Utils import get_project_dir_path

def open_file(root, btn_text, input_dir):
    btn_text.set("Loading...")
    file = askopenfile(parent=root, mode='rb', title="Choose a file", 
            filetypes=[("PNG file", ".png"), ("JPEG file", ".jpeg"), ("JPG file", ".jpg"), ])
    if file:
        name = "user_image"
        clear_directory(input_dir)
        img = Image.open(io.BytesIO(file.read()))
        #img = img.resize((320, 240))
        img.save(os.path.join(input_dir, f"{name}.png"))
        print("\nFile was successfully loaded.")
    btn_text.set("Browse")
    

def start_process(root, frame, btn_text, task_type, progress_bar, per_txt):
    print("\nProcess as started...")
    progress_bar['value'] = 0
    root.update_idletasks()
    if task_type == "Road Connectivity":
        segmentation_flow.main(gui_root=root, bar=progress_bar, txt=per_txt)
        # Display processed image
        proj_dir = get_project_dir_path()
        output_dir = os.path.join(proj_dir, "assets/output_dir")
        filename = os.listdir(output_dir)[0]
        proc_img = Image.open(os.path.join(output_dir, filename))
        proc_img = auto_resize(proc_img, proc_img.size)
        proc_img = ImageTk.PhotoImage(proc_img)
        proc_img_label = tk.Label(frame, image=proc_img)
        proc_img_label.image = proc_img
        proc_img_label.grid(column=0, row=0)

        # Display End Text
        end_text = tk.Label(frame, 
            text="Saved in AWS-Hack-Flood-Damage/assets/output_dir",
        )
        end_text.grid(column=0, row=1)
        print("\nProcess is finished!")

    elif task_type == "Damaged Regions":
        classification_flow.main(gui_root=root, bar=progress_bar, txt=per_txt)
        # Display processed image
        proj_dir = get_project_dir_path()
        output_dir = os.path.join(proj_dir, "assets/output_dir")
        filename = os.listdir(output_dir)[0]
        proc_img = Image.open(os.path.join(output_dir, filename))
        proc_img = auto_resize(proc_img, proc_img.size)
        proc_img = ImageTk.PhotoImage(proc_img)
        proc_img_label = tk.Label(frame, image=proc_img)
        proc_img_label.image = proc_img
        proc_img_label.grid(column=0, row=0)

        # Display End Text
        end_text = tk.Label(frame, 
            text="Saved in AWS-Hack-Flood-Damage/assets/output_dir",
        )
        end_text.grid(column=0, row=1)
        print("\nProcess is finished!")
    else:
        print("Task not defined.")
    per_txt.config(text="")
    progress_bar.stop()

def auto_resize(image, size, desired_height=500):
    width, height = size
    aspect_ratio = width/height
    desired_width = int(desired_height*aspect_ratio)
    image = image.resize((desired_width, desired_height))

    return image


def clear_directory(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete {0}. Reason: {1}'.format(file_path, e))
