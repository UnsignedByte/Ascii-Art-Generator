from PIL import Image,ImageDraw,ImageFont
import os

grayscale=[]
unicodeblocks = [(32,126),(174,846),(910,1366),(1421,1479),(5761,5788),(6656,6678),(7680,7957),(8448,8587),(9312,9472),(9696,10495),(10854,10956),(12032,12245),(11200,11208)]
for block in unicodeblocks:
    for i in range(block[0],block[1]+1):
        total=0
        img = Image.new('L', (7,13), (255))
        fnt=ImageFont.truetype("/Library/Fonts/Courier New.ttf", 11)
        d = ImageDraw.Draw(img)
        d.text((0, 0), chr(i),fill=(0),font=fnt)
        for color in img.getdata():
            total+=color
        grayscale.append((total/91,chr(i)))
grayscale.sort(key=lambda x:x[0])
smol=grayscale[0][0]
dif=grayscale[-1][0]-smol
grey=[None]*12751
for a in range(0,12751):
    grey[a]=grayscale[min(range(len(grayscale)), key=lambda i: abs(((grayscale[i][0]-smol)/dif)*255-a/50))][1]

fpath = os.path.dirname(os.path.abspath(__file__))
    
with open(fpath+"/char.txt", "wb") as file:
    file.write(bytes(chr(166).join(list(x for x in grey)), 'UTF-8'))
