import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter.ttk import Frame
from PIL import Image, ImageTk
import os
import sys
from helper import *

CURRENT_DIR = os.getcwd()
INPUT_DIR = os.path.join(CURRENT_DIR, "../../assets/input_dir")

def project_dir_path(proj_dir_name="AWS-Hack-Flood-Damage"):
    current_dir = os.getcwd()
    index = current_dir.find(proj_dir_name, 0, len(current_dir))
    proj_dir_path = current_dir[:index+len(proj_dir_name)]
    return proj_dir_path

def main():
    ### Start of Tkinter Loop ###
    root = tk.Tk()
    root.geometry("600x350")
    root.title("Floodie GUI Application")
    root.iconphoto(False, tk.PhotoImage(file=os.path.join(PROJ_DIR, "assets/images/icon.png")))

    # Creating a frame
    frame = tk.Frame(root)
    frame.pack()

    # Floodie Logo
    logo = Image.open(
        os.path.join(PROJ_DIR, "assets/images", "floodie_no_bg.png")
        )
    logo = logo.resize((400, 80))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(frame, image=logo)
    logo_label.image = logo
    #logo_label.grid(column=1, row=0)
    logo_label.pack(side=tk.TOP)

    # powered by
    T = tk.Label(frame, text="Powered by", justify=tk.CENTER, font=("Arial", 10))
    #T.grid(column=1, row=1, pady=0)
    T.pack(side=tk.TOP)

    # AWS logo 
    aws_logo = Image.open(
        os.path.join(PROJ_DIR, "assets/images", "amazon_sagemaker_lab.png")
        )
    aws_logo = aws_logo.resize((200, 40))
    aws_logo = ImageTk.PhotoImage(aws_logo)
    aws_logo_label = tk.Label(frame, image=aws_logo)
    aws_logo_label.image = aws_logo
    #aws_logo_label.grid(column=1, row=2)
    aws_logo_label.pack(side=tk.TOP)

    # Creating a BOTTOM Frame
    bottom_frame = tk.Frame(root, pady=10)
    bottom_frame.pack(side=tk.BOTTOM)

    # Creating BOTTOM LEFT and RIGHT Frames
    bottom_left_frame = tk.Frame(bottom_frame, width=200, height=200)
    bottom_left_frame.pack(side=tk.LEFT, padx=10)
    bottom_right_frame = tk.Frame(bottom_frame, borderwidth="1p", relief=tk.GROOVE, padx=10, pady=10)
    bottom_right_frame.pack(side=tk.RIGHT, padx=10)

    # Create a canvas in BOTTOM LEFT FRAME
    canvas_BL = tk.Canvas(bottom_left_frame, height=400, width=300)
    canvas_BL.pack(side=tk.TOP)
    #canvas_BL.grid(columnspan=2, rowspan=3)

    # Creating a frame inside canvas_BL
    canvas_BL_frame = tk.Frame(canvas_BL)
    canvas_BL_frame.grid(column=0, row=0, padx=10, pady=10)


    # WIDGET: Choose a File
    choose_T = tk.Label(canvas_BL_frame, text="Choose a file:", font=("Arial", 11), padx=10)
    choose_T.grid(column=0, row=0)

    # WIDGET: Browse button
    browse_text = tk.StringVar()
    browse_text.set("Browse")
    browse_btn = tk.Button(canvas_BL_frame, textvariable=browse_text, font=("Calibri", 10),
        command=lambda:open_file(root, browse_text, INPUT_DIR), width=16, bd="1.5p")
    browse_btn.grid(column=1, row=0,)

    # WIDGET: Select a Task
    task_T = tk.Label(canvas_BL_frame, text="Select a task:", font=("Arial", 11),)
    task_T.grid(column=0, row=1)

    # WIDGET: Combobox
    task_type = tk.StringVar()
    task_dropdown = ttk.Combobox(canvas_BL_frame, width=17, textvariable=task_type)
    task_dropdown['values'] = (
        "Road Connectivity",
        "Damaged Regions",
    )
    task_dropdown.current(0)
    task_dropdown.grid(column=1, row=1, pady=10)

    # WIDGET: Progress Bar and Percentage text
    progress_bar = ttk.Progressbar(canvas_BL_frame, orient=HORIZONTAL, length=185, mode="determinate")
    progress_bar.grid(columnspan=2, row=3, pady=10)
    percent_text = tk.Label(canvas_BL_frame, text="")
    percent_text.grid(columnspan=2, row=4)


    # WIDGET: Start Button
    start_btn_text = tk.StringVar()
    start_btn_text.set("Start Process")
    start_btn = tk.Button(canvas_BL_frame, textvariable=start_btn_text, font=("Calibri", 10),
        command=lambda:start_process(root, bottom_right_frame, start_btn_text, task_type.get(), progress_bar, percent_text),
        width=25,
    )
    start_btn.grid(columnspan=2, row=2)

    # WIDGET: Blank Image Text
    blank_img_text = tk.Label(bottom_right_frame,
        text="Your processed image will be displayed here",
        font=("Arial", 11),
        wraplength=200,
    )
    blank_img_text.grid(column=0, row=0)    

    #progress_bar.start(10)

    root.mainloop()
    ### End of Tkinter Loop ###

if __name__ == "__main__":
    ### Get Project directory ###
    PROJ_DIR = project_dir_path()

    ### Create Input and Output directories ###
    input_dir = os.path.join(PROJ_DIR, "assets/input_dir")
    output_dir = os.path.join(PROJ_DIR, "assets/output_dir")
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print("Created directory: {}".format(input_dir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print("Created directory: {}".format(output_dir))
    
    ### Call main function ###
    main()