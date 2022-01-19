from PIL import Image
from make_predictions import make_predictions
import os
#inputing image to split into pieces
filename = 'Floods.jpg'
name, ext = os.path.splitext(filename)

img = Image.open('inputdir/'+filename)
width,height = img.size
# piece slicing the image
for xi in range(0,width,400):
    for yi in range(0,height,300):
        box = (xi,yi,
        xi+400 if xi+400 <  width else  width - 1,
        yi+300 if yi+300 < height else height - 1)

        out = os.path.join('outputdir', f'{name}_{xi}_{yi}{ext}')
        print('%s %s'%(filename,box))
        current_img = img.crop(box)  # save the pieces as output
        get_pred = make_predictions(current_img)

print('Image splitted succesfully')

deletion = int(input('Enter 0 to clear the output directory: '))
if deletion == 0:
    dir = 'outputdir/'
    for files in os.listdir(dir):
        os.remove(os.path.join(dir, files))
    print('*'*10+'Output directory is cleared'+'*'*10)