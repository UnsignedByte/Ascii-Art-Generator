# @Author: Edmund Lam <edl>
# @Date:   15:53:50, 15-Oct-2018
# @Filename: Black&White.py
# @Last modified by:   edl
# @Last modified time: 22:12:02, 15-Oct-2018
from PIL import Image,ImageDraw,ImageFont,ImageEnhance
import os
import math
#grey=list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
fpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def sigmoidSquish(x):
    return 1/(1+math.e**(x/-100000))

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def GreyScale(img, max, fsize):
    w,h=img.size
    h/=(9/6)
    if max is not None:
        f = math.sqrt(max/(h*w))
        w *=f
        h *=f
    w = math.floor(w)
    h = math.floor(h)
    enhancement = ((-sigmoidSquish(w*h)+1)+1)**6
    print("IMG Sharpness factor: "+str(enhancement))

    out = getLines(ImageEnhance.Sharpness(img.resize((w,h), Image.ANTIALIAS)).enhance(enhancement));

    imgnew = Image.new('L', (w*6, len(out.splitlines())*9), (255))
    fnt=ImageFont.truetype("/Library/Fonts/Courier New.ttf", 10)
    d = ImageDraw.Draw(imgnew)
    d.multiline_text((0, -10), out,fill=(0),font=fnt,spacing=0)
    if fsize !=(6, 9):
        w,h=img.size
        h/=(fsize[1]/fsize[0])
        if max is not None:
            f = math.sqrt(max/(h*w))
            w *=f
            h *=f
        w = math.floor(w)
        h = math.floor(h)
        enhancement = ((-sigmoidSquish(w*h)+1)+1)**6
        print("TEXT Sharpness factor: "+str(enhancement))

        out = getLines(ImageEnhance.Sharpness(img.resize((w,h), Image.ANTIALIAS)).enhance(enhancement));
    return (imgnew, out)

def getLines(img):
    w,h=img.size
    line=""
    lines=1
    out=""
    for color in img.getdata():
        if len(line)==w:
            out=out+"\n"+line.rstrip()
            line=""
            lines+=1
        try:
            r=color[0]
            g=color[1]
            b=color[2]
            #0.3*r + 0.59*g + 0.11*b
            line=line+grey[round(((0.2126*r + 0.7152*g + 0.0722*b)/255)*(len(grey)-1))]
        except TypeError:
            line=line+grey[round((color/255)*(len(grey)-1))]
    return out


while True:
    res = input("Ascii or Unicode:")
    if res.lower() == "ascii":
        grey = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'. ")
    elif res.lower() == "unicode":
        with open(fpath+"/char.txt", "rb") as file:
            grey=file.read().decode('UTF-8').split(chr(166))
    else:
        print("Invalid Input")
        exit(0)
    res = input("Maximum Characters (type \"inf\" for no max):")
    if res.lower() == "inf":
        max = None
    elif isInt(res.lower()):
        max = int(res)
    else:
        print("Invalid Input")
        exit(0)
    filename=input("FileName:")
    try:
        image = Image.open(fpath+'/input/%s' % filename)
        if filename.split(".")[1]=="gif":
            gif=[]
            mypalette = image.getpalette()
            while True:
                try:
                    image.putpalette(mypalette)
                    new_im = Image.new("RGBA", image.size)
                    new_im.paste(image)
                    gif.append(GreyScale(new_im, max)[0])
                    image.seek(image.tell() + 1)
                except EOFError:
                    break
            gif[0].save(fpath+'/output/%s.gif' %(filename.split(".")[0]),save_all=True,append_images=gif[1:])
        else:
            try:
                rgb_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
                rgb_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
            except ValueError:
                rgb_image = image
            res = input("Text font width, height (separate with space), \"def\" for default:")
            if res.lower() == "def":
                fsize = (6, 9)
            else:
                try:
                    fsize = tuple(map(int, res.split(",")))
                except Exception:
                    print("Invalid Input")
                    exit(0)
            rgb_image.convert('RGB')
            tupg = GreyScale(rgb_image, max, fsize)
            tupg[0].save(fpath+"/output/%s.png" %(filename.split(".")[0]))
            print("%s characters written." %len(tupg[1]))

            with open(fpath+"/output_text/%s.txt" %(filename.split(".")[0]), "w") as f:
                f.write(tupg[1])
    except Exception:
        print("incompatible/missing file")
