# AWS-Hack-Flood-Damage
## About
This project was made for AWS Disaster Response Hackathon. This repository contains code for identifying damaged regions in an aerial image. Identifying damaged objects (such as roads and buildings) in aerial images can be helpful to disaster-response organizations in responding to natural calamities faster and more efficiently. This project focuses on how organizations can respond better to damage inflicted by hurricanes and floods. The datasets used to train models contain aerial images of zones affected by hurricane Harvey.

## Functionality
The project is focused on the response phase of a disaster life cycle. It provides two basic functions. 
* **Road Connectivity: *Identify flooded and non-flooded roads.*** This can be useful for various tasks (transportation and mobility) such as planning a route to a particular location when some roads are inundated with water. It gives a basic overview of connectivity of roads which flooded and non-flooded. 
* **Damaged Regions: *Identify damaaged regions (broken houses or flooded parts).*** This can be useful to organization in estimating which areas in a town or city have been affected the most, thereby allowing them to properly direct their efforts. 
* **Basic Graphical User Interface.**</b> This allows users to upload their aerial images (from UAV or Satellite) and easily implement the above mentioned functions. The GUI application was made with the Tkinter module in python. More features can be added to the GUI implemented in the future. The image below is the starting screen of the app. 
<p align="center">
  <img src="assets/images/GUI_init_screen.png" style="height: 300px; width: 547px;"/>
</p>

## Dependencies 
The poject relies on the following dependencies. Make sure all of the packages mentioned below are installed.
1. [TensorFlow](https://www.tensorflow.org/)
2. [Numpy](https://numpy.org/) 
3. [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/)
4. [Tkinter](https://docs.python.org/3/library/tkinter.html)
5. [Tqdm](https://github.com/tqdm/tqdm)

## Models
| Sl. no. | Name | Description | Architecture | Task Type | Dataset | 
| --- | --- | --- | --- | --- | --- |
| 1. | **U-NET-like model.** | Used for segmentation done on aerial images to identify flooded and non-flooded roads | Similar to U-Net architecture. See [here](https://github.com/hamdaan19/AWS-Hack-Flood-Damage/blob/main/scripts/unet_xception_model.py) for more details. | Semantic Segmentation | [FloodNet dataset](https://github.com/BinaLab/FloodNet-Challenge-EARTHVISION2021) | 
| 2. | **Xception model.** | used for binary classification of 128x128 sized images as damaged or not damaged. | It uses the same architecture of Xception but with the last layer substituted with a layer of 2 fully connected neurons with a softmax activation. Transfer Learning was implemented to use Xception on binary classification problem. | Binary Classification | [Hurricane Damage dataset](https://www.kaggle.com/kmader/satellite-images-of-hurricane-damage) |
