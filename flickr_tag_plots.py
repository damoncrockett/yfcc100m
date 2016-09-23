import pandas as pd
import numpy as np
from shapely.geometry import Point
from PIL import Image, ImageDraw
import glob
import os

DIR = "/data/damoncrockett/flickr_data/raw/concepts/"
FOLDER = "/data/damoncrockett/flickr/tag_plots/"

thumb_side = 160

counter = -1
for file in glob.glob(os.path.join(DIR,"*.csv")):
    counter+=1
    concept = os.path.splitext(os.path.basename(file))[0]
    try:
        os.mkdir(FOLDER+concept)
    except:
        pass
    
    df = pd.read_csv(file)
    df = df[~df.dl_url.str.contains("@")] # damn videos with no extension

    # if weighting...
    m = len(df)
    pctile = m/100
    heavy = 99
    light = 1
    sample_weights = list(np.repeat(heavy,pctile)) + list(np.repeat(light,m-pctile))
    
    if df[concept].dtype=='O': # to get the variants
        df = df[[concept,'dl_url']][df[concept]!="variant"]
    hits = df.sample(n=625)
    hits.sort(concept,inplace=True,ascending=False)
    #hits = hits.sample(n=625,weights=sample_weights)
    hits.reset_index(drop=True,inplace=True)
    n = len(hits.index)

    side = int(round(np.sqrt(n))) + 5
    canvas = Image.new('RGB',(side * thumb_side, side * thumb_side),(50,50,50))
    x,y = range(side) * side, np.repeat(range(side),side)
    grid_list = pd.DataFrame(x,columns=['x'])
    grid_list['y'] = y
        
    point = []
    l = len(grid_list.index)
    for i in range(l):
        point.append(Point(grid_list.x.loc[i],grid_list.y.loc[i]))
    grid_list['point'] = point
    open_grid = list(grid_list.point)
    
    import requests
    import shutil
    from skimage.io import imread

    exemplar = Point(int(round(side/2)),int(round(side/2)))
    
    for k in range(n):
        path = FOLDER + concept + "/" + hits.dl_url.loc[k].split('/',5)[4]
        r = requests.get(hits.dl_url.loc[k],stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        img = imread(path)
        if len(img.shape) == 3: # to elim the blank return img, which is bw
            break
    
    im = Image.open(path)
    im.thumbnail((thumb_side,thumb_side),Image.ANTIALIAS)
    x = int(exemplar.x) * thumb_side
    y = int(exemplar.y) * thumb_side
    canvas.paste(im,(x,y))
    open_grid.remove(exemplar)

    for j in range(k+1,n):
        path = FOLDER + concept + "/" + hits.dl_url.loc[j].split('/',5)[4]
        print counter,j, path

        r = requests.get(hits.dl_url.loc[j],stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

        im = Image.open(path)
        img = imread(path)
        if len(img.shape) == 3: # to elim the blank return img, which is bw
            im.thumbnail((thumb_side,thumb_side),Image.ANTIALIAS)
            height = im.height
            width = im.width
            position = [width - int(round(width/3)),int(round(height/8))]
            draw = ImageDraw.Draw(im)
            draw.text(position,str(hits[concept].loc[j]),fill="white")
        
            closest_open = min(open_grid,key=lambda x: exemplar.distance(x))
            x = int(closest_open.x) * thumb_side
            y = int(closest_open.y) * thumb_side
            canvas.paste(im,(x,y))
            open_grid.remove(closest_open)
        
    canvas.save(FOLDER+concept+".png")
