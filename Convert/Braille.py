# @Author: Edmund Lam <edl>
# @Date:   17:50:23, 15-Oct-2018
# @Filename: Braille.py
# @Last modified by:   edl
# @Last modified time: 10:45:11, 16-Oct-2018

CONST_WHITE = 0.2

BRAILLES = [chr(i) for i in range(int('2800', 16), int('2900', 16))]

from PIL import Image,ImageDraw,ImageFont,ImageEnhance
import os
import math
fpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def sigmoidSquish(x):
    return 1/(1+math.e**(x/-100000))

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def CALC_WHITE(x):
    if x < CONST_WHITE: return 0
    elif round(x) == 0: return 1
    else: return 2

def Braille(img, max, fsize):
    w,h=img.size
    out=""
    h/=fsize[1]/fsize[0] * 1/2
    if max is not None:
        f = math.sqrt(max/(h/4*w/2))
        w *=f
        h *=f
    w = round(w//2*2)
    h = round(h//4*4)

    enhancement = ((-sigmoidSquish(w*h)+1)+1)**7
    img = ImageEnhance.Sharpness(img.resize((w,h), Image.ANTIALIAS)).enhance(enhancement)
    print("Sharpness factor: "+str(enhancement))
    colors = []
    for color in img.getdata():
        try:
            r=color[0]
            g=color[1]
            b=color[2]
            #0.3*r + 0.59*g + 0.11*b
            colors.append(1-((0.2126*r + 0.7152*g + 0.0722*b)/255))
        except TypeError:
            colors.append(1-color/255)

    for i in range(h//4):
        line = ""
        for j in range(w//2):
            b = i*4*w+j*2
            aa, bb = colors[b:b+2]
            cc, dd = colors[b+w:b+w+2]
            ee, ff = colors[b+2*w:b+2*w+2]
            gg, hh = colors[b+3*w:b+3*w+2]

            if list(map(lambda x:CALC_WHITE(x), [aa, bb, cc, dd, ee, ff, gg, hh])) == [1]*8:
                line+=BRAILLES[64]
            else:
                line+=BRAILLES[64*(round(hh)*2+round(gg))+int(''.join(list(map(lambda x:str(round(x)), [ff,dd,bb,ee,cc,aa]))), 2)]
        out+=line.rstrip('\u2800')+"\n"

    return out.strip("\n")

while True:
    res = input("Maximum Characters (type \"inf\" for no max):")
    if res.lower() == "inf":
        max = 4000000
    elif isInt(res.lower()):
        max = int(res)
    else:
        print("Invalid Input")
        exit(0)
    filename=input("FileName:")
    try:
        image = Image.open(fpath+'/input/%s' % filename)
        if filename.split(".")[1]=="gif":
            print("gif not supported")
        else:
            try:
                rgb_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
                rgb_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
            except ValueError:
                rgb_image = image

            res = input("Text font width, height (separate with space), \"def\" for default:")
            if res.lower() == "def":
                fsize = (9, 18)
            else:
                try:
                    fsize = tuple(map(int, res.split(",")))
                except Exception:
                    print("Invalid Input")
                    exit(0)

            rgb_image.convert('RGB')

            tupg = Braille(rgb_image, max, fsize)
            print("%s characters written." %len(tupg))

            with open(fpath+"/output_text/%s.txt" %(filename.split(".")[0]), "w") as f:
                f.write(tupg)
    except Exception:
        print("incompatible/missing file")
