from PIL import Image
import os
#inputing image to split into pieces
filename = 'Floods.jpg'
chopsizing = 100
name, ext = os.path.splitext(filename)

img = Image.open('inputdir/'+filename)
width,height = img.size
# piece slicing the image
for xi in range(0,width,chopsizing):
    for yi in range(0,height,chopsizing):
        box = (xi,yi,
        xi+chopsizing if xi+chopsizing <  width else  width - 1,
        yi+chopsizing if yi+chopsizing < height else height - 1)

        out = os.path.join('outputdir', f'{name}_{xi}_{yi}{ext}')
        print('%s %s'%(filename,box))
        img.crop(box).save(out)  # save the pieces as output

print('Image splitted succesfully')

deletion = int(input('Enter 0 to clear the output directory: '))
if deletion == 0:
    dir = 'outputdir/'
    for files in os.listdir(dir):
        os.remove(os.path.join(dir, files))
    print('*'*10+'Output directory is cleared'+'*'*10)