BASE_DIR = "/data/damoncrockett/downtown_SD_Flickr"

import glob
import os
from PIL import Image

for i in range(1,5):
    counter = -1
    for file in glob.glob(os.path.join(BASE_DIR+"/images_sliced_"+str(i)+"/","*.png")):
        counter+=1
        try:
            im = Image.open(file)
            w = im.width
            h = im.height

            if ((w<4) or (h<4)):
                print "small"
            else:
                im_filename = BASE_DIR+"/images_sliced_cropped/"+os.path.basename(file)
                if w > h:
                    im = im.crop((0,0,h,h))
                    im.thumbnail((4,4),Image.ANTIALIAS)
                    im.save(im_filename)
                elif h > w:
                    im = im.crop((0,h-w,w,h))
                    im.thumbnail((4,4),Image.ANTIALIAS)
                    im.save(im_filename)
                elif h == w:
                    im.thumbnail((4,4),Image.ANTIALIAS)
                    im.save(im_filename)
                print i,counter 

        except:
            print "err"
