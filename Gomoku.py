from PIL import Image, ImageFont, ImageDraw
import random
import re
import time
import os
 
"""""
返回的Json应当包含元素：{"state" : "running/waiting", "nowOperator": playerID , "active":True/False, "legal":True/False,
            "errorBack":"Str", "finish":True/False, "winner":playerID, "gameInfo":"Str", "lastOperationTime": int
            "normalBack":"Str"}
"""""

path = os.getcwd()
idx = [1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']
num = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
Const = 50
D = 36
chessBoard = Image.open(f"{path}/Data/Gomoku/chessboard.png")
fontPath = rf"{path}/Data/Font/GB2312.ttf"
font = ImageFont.truetype(fontPath, 25)
black = Image.open(f"{path}/Data/Gomoku/black.png")
white = Image.open(f"{path}/Data/Gomoku/white.png")
black_last = Image.open(f"{path}/Data/Gomoku/black_last.png")
white_last = Image.open(f"{path}/Data/Gomoku/white_last.png")


def getPos(x, y):
    return (x-1)*D + Const , (y-1)*D + Const


class Gomoku:
    def __init__(self, chessBoardID):
        #   初始化棋盘
        self.chessBoardID = chessBoardID
        self.imagePath = f"{path}/Data/Gomoku/chessBoard-{chessBoardID}.png"
        self.image = Image.new(mode='RGB', size=(590,590), color="white")
        self.image.paste(chessBoard, (Const+10,Const+10))
        dr = ImageDraw.Draw(self.image)
        for i in range(1, 16):
            x,y = getPos(1,i)
            dr.text((x - 20, y+2),font=font, text=f"{idx[i-1]}",fill="#000000")
        for i in range(1, 16):
            x,y = getPos(i,1)
            dr.text((x + 10, y - 25),font=font, text=f"{idx[i-1]}",fill="#000000")
        self.saveImage()

        #   初始化对局信息
        self.nowOperatorIdx = 0
        self.playerArr = []
        self.state = "waiting"
        self.operationType = "NULL"
        self.backMsg = "NULL"
        self.winner = 0
        self.active = False
        self.winnerScore = 25
        self.scoreChangeList = {}
        self.gameInfo = "NULL"
        self.autoArgument = None
        self.downNumber = 0
        self.lastOperation = [0, 0, 0]
        self.lastOperationTime = time.time()
        self.chessBoard = []
        for i in range(0,16):
            self.chessBoard.append([])
            for j in range(0,16):
                self.chessBoard[i].append(0)

    def saveImage(self):
        self.image.save(self.imagePath)

    def checkResult(self, y, x):
        print(f"y = {y}, and x = {x}")
        print(f"Dict y = {num.get(str(y), -1)}, x = {num.get(str(x), -1)}")
        x = int(num[str(x)])
        y = int(num[str(y)])
        print(f"检索棋盘位置[{y}][{x}]")
        Type = self.chessBoard[x][y]
        number = 1
        tempx,tempy = x-1,y
        while tempx>=1 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempx -= 1
        tempx = x+1
        while tempx<=15 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempx += 1

        if number >=5 :
            return True

        number = 1

        tempx,tempy = x,y-1
        while tempy>=1 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempy -= 1
        tempy = y+1
        while tempy<=15 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempy += 1

        if number >=5 :
            return True
        
        # ---------------------
        number = 1
        tempx,tempy = x-1,y-1
        while tempx>=1 and tempy>=1 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempx -= 1
            tempy -= 1
        tempx = x+1
        tempy = y+1
        while tempx<=15 and tempy<=15 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempx += 1
            tempy += 1

        if number >=5 :
            return True

        number = 1

        tempx,tempy = x+1,y-1
        while tempy>=1 and tempx<=15 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempy -= 1
            tempx += 1
        tempx = x-1
        tempy = y+1
        while tempy<=15 and tempx>=1 and self.chessBoard[tempx][tempy] == Type:
            number += 1
            tempy += 1
            tempx -= 1

        if number >=5 :
            return True
        return False

    def checkLocation(self, y, x):
        x = int(num[str(x)])
        y = int(num[str(y)])
        return self.chessBoard[x][y] == 0

    def moveInChess(self, Y, X):
        Y = int(num[str(Y)])
        X = int(num[str(X)])
        lastType = self.lastOperation[0]
        x,y = getPos(self.lastOperation[1], self.lastOperation[2])
        if lastType == 0:
            x,y = getPos(X,Y)
            self.image.paste(black_last, (x, y))
            self.lastOperation = [1,X,Y]
            self.chessBoard[X][Y] = 1
            self.saveImage()
            return
        if lastType == 1:
            self.image.paste(black, (x, y))
            x,y = getPos(X,Y)
            self.image.paste(white_last, (x, y))
            self.lastOperation = [2,X,Y]
            self.chessBoard[X][Y] = 2
        else:
            self.image.paste(white, (x, y))
            x,y = getPos(X,Y)
            self.image.paste(black_last, (x, y))
            self.lastOperation = [1,X,Y]
            self.chessBoard[X][Y] = 1
        self.saveImage()
        
    def getFullPath(self):
        return f"file:///{self.imagePath}"

    def getLastOperationTime(self):
        return self.lastOperationTime

    def updateTime(self):
        self.lastOperationTime = time.time()

    def getNowOperator(self):
        if len(self.playerArr) < 2:
            return -1
        return self.playerArr[self.nowOperatorIdx]

    def updateArgument(self, Str):
        lis = Str.split(' ')
        self.autoArgument = []
        for arg in lis:
            self.autoArgument.append(arg)

    def getPlayerList(self):
        return self.playerArr

    def makeDict(self):
        Dict = {"state": self.state, "nowOperator": self.getNowOperator(), "active": self.active,"operationType":self.operationType,
                "backMsg":self.backMsg, "winner": self.winner, "scoreChangeList": self.scoreChangeList
                , "lastOperationTime": self.lastOperationTime, "imagePath":self.getFullPath()}
        return Dict

    def reset(self):
        self.__init__(self.chessBoardID)

    def running(self, playerID, Str):
        self.updateArgument(Str)
        if Str == "五子棋投降" and self.state == "running":
            self.active = True
            self.operationType = "玩家投降"
            for qq in self.playerArr:
                if qq == playerID:
                    self.scoreChangeList[qq] = -self.winnerScore
                else:
                    self.scoreChangeList[qq] = self.winnerScore
                    self.winner = qq
            return self.makeDict()
        if Str == "五子棋掀桌" and self.state == "running":
            self.active = True
            if time.time() - self.lastOperationTime < 2 * 60:
                self.operationType = "不合法"
                self.backMsg = "距离上一次合法操作未到2分钟，无法掀桌"
                return self.makeDict()
            self.operationType = "掀桌"
            for qq in self.playerArr:
                if qq == self.getNowOperator():
                    self.scoreChangeList[qq] = -30
                else:
                    self.scoreChangeList[qq] = 25
            return self.makeDict()
        if self.state == "running" and Str == "五子棋对局信息":
            self.active = True
            self.operationType = "询问对局信息"
            self.backMsg = "整理中...请稍等..."
            return self.makeDict()
        if Str == "加入五子棋":
            self.active = True
            if self.playerArr.count(playerID) != 0:
                self.operationType = "不合法"
                self.backMsg = "你已经在里面了..."
                return self.makeDict()
            if self.state == "running":
                self.operationType = "不合法"
                self.backMsg = "对局已经开始了...等下一把吧"
                return self.makeDict()
            self.playerArr.append(playerID)
            self.operationType = "加入对局"
            self.backMsg = f"加入成功！\n玩家列表{self.playerArr}"
            self.updateTime()
            if len(self.playerArr) == 2:
                self.operationType = "对局开始"
                self.backMsg += "\n人数已满，对局开始！"
                self.state = "running"
                self.nowOperatorIdx = 0
                if random.randint(0,1) == 1:
                    temp = self.playerArr[0]
                    self.playerArr[0] = self.playerArr[1]
                    self.playerArr[1] = temp
            return self.makeDict()
        if Str == "离开五子棋" and self.playerArr.count(playerID):
            self.active = True
            self.updateTime()
            if self.state == "running":
                self.operationType = "不合法"
                self.backMsg = "对局已开始，想提前离开就只能投降"
                return self.makeDict()
            self.operationType = "离开对局"
            self.playerArr.remove(playerID)
            self.backMsg = "好的"
            return self.makeDict()
        if self.state == "running" and self.getNowOperator() == playerID and (re.match("落子.*", Str) or re.match("LZ.*", Str)):
            self.active = True
            if  len(self.autoArgument[0]) != 4 or num.get(str(self.autoArgument[0][2]), 0) == 0 or num.get(str(self.autoArgument[0][3]), 0) == 0:
                self.operationType = "不合法"
                self.backMsg = "你坐标参数不对吧"
                return self.makeDict()

            if not self.checkLocation(self.autoArgument[0][2], self.autoArgument[0][3]):
                self.operationType = "不合法"
                self.backMsg = "你选的位置已经有棋子啦"
                return self.makeDict()
            self.updateTime()
            self.operationType = "落子"
            self.downNumber += 1
            self.nowOperatorIdx += 1
            self. nowOperatorIdx %= 2
            self.backMsg = "操作成功！正在更新对局信息..."
            self.moveInChess(self.autoArgument[0][2], self.autoArgument[0][3])
            if self.checkResult(self.autoArgument[0][2], self.autoArgument[0][3]):
                self.operationType = "对局结束"
                self.backMsg = "游戏结束！"
                self.winner = playerID
                for qq in self.playerArr:
                    if qq == playerID:
                        self.scoreChangeList[qq] = self.winnerScore
                    else:
                        self.scoreChangeList[qq] = -self.winnerScore
                return self.makeDict()
            if self.downNumber == 225:
                self.operationType = "平局"
            return self.makeDict()
        self.active = False
        return self.makeDict()


if __name__ == "__main__":
    T = Gomoku(123)
    T.running(1,"加入五子棋")
    T.running(2,"加入五子棋")

    T.running(1, "落子91")
    T.running(2, "落子A1")
    T.running(1, "落子92")
    T.running(2, "落子A2")
    T.running(1, "落子93")
    T.running(2, "落子A3")
    
    T.running(1, "落子A4")
    T.running(2, "落子94")
    T.running(1, "落子A5")
    T.running(2, "落子95")
    T.running(1, "落子A6")
    T.running(2, "落子96")
    
    T.running(1, "落子97")
    T.running(2, "落子A7")
    T.running(1, "落子98")
    T.running(2, "落子A8")
    T.running(1, "落子99")
    T.running(2, "落子A9")
    
    T.running(1, "落子AA")
    T.running(2, "落子9A")
    T.running(1, "落子AB")
    T.running(2, "落子9B")
    T.running(1, "落子AC")
    T.running(2, "落子9C")
    
    T.running(1, "落子9D")
    T.running(2, "落子AD")
    T.running(1, "落子9E")
    T.running(2, "落子AE")
    T.running(1, "落子9F")
    T.running(2, "落子AF")
    # ----------------------------
    
    T.running(1, "落子71")
    T.running(2, "落子81")
    T.running(1, "落子72")
    T.running(2, "落子82")
    T.running(1, "落子73")
    T.running(2, "落子83")
    
    T.running(1, "落子84")
    T.running(2, "落子74")
    T.running(1, "落子85")
    T.running(2, "落子75")
    T.running(1, "落子86")
    T.running(2, "落子76")
    
    T.running(1, "落子77")
    T.running(2, "落子87")
    T.running(1, "落子78")
    T.running(2, "落子88")
    T.running(1, "落子79")
    T.running(2, "落子89")
    
    T.running(1, "落子8A")
    T.running(2, "落子7A")
    T.running(1, "落子8B")
    T.running(2, "落子7B")
    T.running(1, "落子8C")
    T.running(2, "落子7C")
    
    T.running(1, "落子7D")
    T.running(2, "落子8D")
    T.running(1, "落子7E")
    T.running(2, "落子8E")
    T.running(1, "落子7F")
    T.running(2, "落子8F")


    
