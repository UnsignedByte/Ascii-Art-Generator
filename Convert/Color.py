# @Author: Edmund Lam <edl>
# @Date:   15:53:54, 15-Oct-2018
# @Filename: Color.py
# @Last modified by:   edl
# @Last modified time: 16:04:21, 15-Oct-2018


from PIL import Image,ImageDraw,ImageFont
import os
from colorsys import rgb_to_hls, hls_to_rgb

fpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(fpath+"/char.txt", "rb") as file:
    grey=file.read().decode('UTF-8').split(chr(166))

def Convert(img):
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
    currx = 0
    curry = 0
    imgnew = Image.new('RGB', (w*6, h*9), (255,255,255))
    fnt=ImageFont.truetype("/Library/Fonts/Courier New.ttf", 10)
    d = ImageDraw.Draw(imgnew)
    for color in img.getdata():
        if currx==w*6:
            curry+=9
            currx=0
        try:
            r=color[0]
            g=color[1]
            b=color[2]
            h, l, s = rgb_to_hls(r/255, g/255, b/255)
            col = tuple(map(lambda x: round(x*255), hls_to_rgb(h, l, 1)))
            d.text((currx, curry), grey[round(((0.2126*r + 0.7152*g + 0.0722*b)/255)*(len(grey)-1))], fill=col, font=fnt)
        except TypeError as e:
            print(e)
            d.text((currx, curry), grey[round((color/255)*(len(grey)-1))], fill=hls_to_rgb(h, l, 1), font=fnt, spacing=0)
        finally:
            currx+=6
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
    #try:
    image = Image.open(fpath+'/input/%s' % filename)
    if filename.split(".")[1]=="gif":
        gif=[]
        mypalette = image.getpalette()
        while True:
            try:
                image.putpalette(mypalette)
                new_im = Image.new("RGBA", image.size)
                new_im.paste(image)
                gif.append(Convert(new_im))
                image.seek(image.tell() + 1)
            except EOFError:
                break
        gif[0].save(fpath+'/output/%s.gif' %(filename.split(".")[0]),save_all=True,append_images=gif[1:])
        Image.open(fpath+'/output/%s.gif' %(filename.split(".")[0])).show()
    else:
        rgb_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
        rgb_image.paste(image, (0, 0), image)              # Paste the image on the background. Go to the links given below for details.
        rgb_image.convert('RGB')
        Convert(rgb_image).save(fpath+"/output/%s.png" %(filename.split(".")[0]))
        Image.open(fpath+'/output/%s.png' %(filename.split(".")[0])).show()
    #except Exception:
 #       print("incompatible/missing file")
