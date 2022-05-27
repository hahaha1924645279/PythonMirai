from PIL import Image, ImageFont, ImageDraw
import os
stk = 0 

def CreateImg(text, fontSize=15):
    global stk
    liens = text.split('\n')
    #画布颜色
    im = Image.new("RGB", (480, len(liens)*(fontSize+5)), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    fontPath = r"./Data/Font/GB2312.ttf"
    font = ImageFont.truetype(fontPath, fontSize)
    #文字颜色
    dr.text((0, 0), text, font=font, fill="#000000")
    path = os.getcwd()
    stk += 1
    im.save(f"{path}/Data/{stk}.jpg")
    stk -= 1
    temp = rf"file:///{path}/Data/{stk+1}.jpg"
    path = ""
    for i in temp:
        if i == '\\':
            path += '/'
        else:
            path += i
    return path
 