# from PIL import Image, ImageFont, ImageDraw


# idx = [1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']
# Const = 50
# D = 36

# def getPos(x, y):
#     return (x-1)*D + Const , (y-1)*D + Const


# ans = Image.new(mode='RGB', size=(590,590), color="white")
# chessBoard = Image.open("./Data/Gomoku/chessboard.png")
# fontPath = r"GB2312.ttf"
# font = ImageFont.truetype(fontPath, 20)
# dr = ImageDraw.Draw(ans)
# black = Image.open("./Data/Gomoku/black.png")
# white = Image.open("./Data/Gomoku/white.png")
# black_last = Image.open("./Data/Gomoku/black_last.png")
# white_last = Image.open("./Data/Gomoku/white_last.png")
# ans.paste(chessBoard, (Const+10,Const+8))
# for i in range(1, 16):
#     x,y = getPos(1,i)
#     dr.text((x - 20, y+2),font=font, text=f"{idx[i-1]}",fill="#000000")
# for i in range(1, 16):
#     x,y = getPos(i,1)
#     dr.text((x + 10, y - 25),font=font, text=f"{idx[i-1]}",fill="#000000")

# ans.save("test.png")

lis = [15,16,17,15]
print(lis.count(15))