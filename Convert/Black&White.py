# @Author: Edmund Lam <edl>
# @Date:   15:53:50, 15-Oct-2018
# @Filename: Black&White.py
# @Last modified by:   edl
# @Last modified time: 16:04:33, 15-Oct-2018
from PIL import Image,ImageDraw,ImageFont
import os
#grey=list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
fpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(fpath+"/char.txt", "rb") as file:
    grey=file.read().decode('UTF-8').split(chr(166))

def GreyScale(img):
    line=""
    lines=1
    w,h=img.size
    out=""
    if w>1620:
        h=(h/w)*1620
        w=1620
    if h>1620:
        w=(w/h)*1620
        h=1620
    w=round(w)
    h=round(h/(9/6))
    img=img.resize((w,h), Image.ANTIALIAS)
    for color in img.getdata():
        if len(line)==w:
            out=out+"\n"+line
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
    imgnew = Image.new('L', (w*6, lines*9), (255))
    fnt=ImageFont.truetype("/Library/Fonts/Courier New.ttf", 10)
    d = ImageDraw.Draw(imgnew)
    d.multiline_text((0, -10), out,fill=(0),font=fnt,spacing=0)
    return imgnew

while True:
    res = input("Ascii or Unicode:")
    if res.lower() == "ascii":
        grey = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    elif res.lower() == "unicode":
        pass
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
                    gif.append(GreyScale(new_im))
                    image.seek(image.tell() + 1)
                except EOFError:
                    break
            gif[0].save(fpath+'/output/%s.gif' %(filename.split(".")[0]),save_all=True,append_images=gif[1:])
            Image.open(fpath+'/output/%s.gif' %(filename.split(".")[0])).show()
        else:
            rgb_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
            rgb_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
            rgb_image.convert('RGB')
            GreyScale(rgb_image).save(fpath+"/output/%s.png" %(filename.split(".")[0]))
            Image.open(fpath+'/output/%s.png' %(filename.split(".")[0])).show()
    except Exception:
        print("incompatible/missing file")
