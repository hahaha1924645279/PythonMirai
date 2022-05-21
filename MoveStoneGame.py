import random
import re
import time

"""""
返回的Json应当包含元素：{"state" : "running/waiting", "nowOperator": playerID , "active":True/False, "legal":True/False,
            "errorBack":"Str", "finish":True/False, "winner":playerID, "gameInfo":"Str", "lastOperationTime": int
            "normalBack":"Str"}
"""""


class MoveStone:
    def __init__(self):
        self.A = random.randint(1, 1000)
        self.B = random.randint(1, 1000)
        while self.A % self.B == 0 or self.B % self.A == 0:
            self.A = random.randint(1, 1000)
            self.B = random.randint(1, 1000)
        self.nowOperatorIdx = 0
        self.playerArr = []
        self.state = "waiting"
        self.legal = True
        self.errorBack = "可以加一下我吗？"
        self.normalBack = "可以加一下我吗？(我男的)"
        self.finish = False
        self.winner = 0
        self.active = False
        self.breakGame = False
        self.winnerScore = 10
        self.scoreChangeList = {}
        self.gameInfo = "可以加一下我吗？我夜间比较能聊"
        self.autoArgument = None
        self.lastOperationTime = time.time()

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

    def updateGameInfo(self):
        Str = f"当前对局信息:\nA:{self.A} B:{self.B}"
        self.gameInfo = Str

    def makeDict(self):
        Dict = {"state": self.state, "nowOperator": self.getNowOperator(), "active": self.active,
                "legal": self.legal, "errorBack": self.errorBack, "normalBack": self.normalBack,
                "breakGame": self.breakGame,
                "finish": self.finish, "winner": self.winner, "scoreChangeList": self.scoreChangeList,
                "gameInfo": self.gameInfo, "lastOperationTime": self.lastOperationTime}
        return Dict

    def reset(self):
        self.A = random.randint(1, 1000)
        self.B = random.randint(1, 1000)
        while self.A % self.B == 0 or self.B % self.A == 0:
            self.A = random.randint(1, 1000)
            self.B = random.randint(1, 1000)
        self.nowOperatorIdx = 0
        self.playerArr = []
        self.state = "waiting"
        self.legal = True
        self.errorBack = "Null"
        self.normalBack = "Null"
        self.finish = False
        self.breakGame = False
        self.winner = 0
        self.scoreChangeList = {}
        self.winnerScore = 10
        self.active = False
        self.gameInfo = "Null"
        self.autoArgument = None
        self.lastOperationTime = time.time()

    def running(self, playerID, Str):
        self.updateArgument(Str)
        self.updateGameInfo()
        if re.match("挪石头掀桌", Str) and self.state != "waiting":
            self.active = True
            if time.time() - self.lastOperationTime < 5*60:
                self.legal = False
                self.errorBack = "距离上一次合法操作未到5分钟，无法掀桌"
            else:
                self.legal = True
                self.breakGame = True
                for qq in self.playerArr:
                    if qq != self.getNowOperator():
                        self.scoreChangeList[qq] = +3
                    else:
                        self.scoreChangeList[qq] = -20
            return self.makeDict()
        if re.match("挪石头投降", Str) and self.state == "running":
            self.active = True
            self.legal = False
            if self.playerArr.count(playerID) == 0:
                self.errorBack = "你没在里面呢..."
            else:
                for qq in self.playerArr:
                    if qq != playerID:
                        self.winner = qq
                        self.scoreChangeList[qq] = 10 - int((self.A + self.B)/200)
                    else:
                        self.scoreChangeList[qq] = int((self.A + self.B)/200) - 10
                self.finish = True
                self.legal = True
                self.normalBack = "你选择了投降"
            return self.makeDict()
        if re.match("挪石头对局信息", Str):
            self.active = True
            self.legal = False
            self.errorBack = self.gameInfo
            if self.state == "waiting":
                self.errorBack = "还没开局，暂无信息"
            return self.makeDict()
        if re.match("离开挪石头", Str):
            self.active = True
            self.legal = False
            if self.playerArr.count(playerID) == 0:
                self.errorBack = "你没在里面呢..."
                return self.makeDict()
            if self.state == "running":
                self.errorBack = "对局已经开始了，你要离开就点投降吧"
                return self.makeDict()
            self.errorBack = "好的，你已离开"
            self.playerArr.remove(playerID)
            return self.makeDict()
        if re.match("加入挪石头", Str):
            self.active = True
            if self.state == "running":
                self.active = False
                self.legal = False
                self.errorBack = "对局已经开始了，等待下一轮吧..."
            else:
                if self.playerArr.count(playerID) == 0:
                    self.legal = True
                    self.active = True
                    self.updateTime()
                    self.playerArr.append(playerID)
                    self.normalBack = f"加入成功！\n玩家列表:{self.playerArr}\n"
                    if len(self.playerArr) == 2:
                        self.state = "running"
                        self.nowOperatorIdx = 0
                        self.normalBack = f"加入成功！\n玩家列表:{self.playerArr}\n人数已满，游戏开始！"
                else:
                    self.active = True
                    self.legal = False
                    self.errorBack = "你已经在对局当中了"
            return self.makeDict()
        if self.getNowOperator() != playerID:
            self.active = False
            return self.makeDict()
        if re.match("A [0-9]+ [0-9]+", Str) and self.state == "running":
            self.active = True
            if int(self.autoArgument[1]) == 0:
                self.legal = False
                self.errorBack = "你给定的值不合法，x应当为正整数"
                return self.makeDict()
            temp1 = int(self.autoArgument[1])
            temp2 = int(self.autoArgument[2])
            if temp1 > self.A or temp1*temp2 > self.B:
                self.legal = False
                self.active = True
                self.errorBack = "你给定的值不合法，超出了所能挪动的数量"
                return self.makeDict()
            self.legal = True
            self.A -= temp1
            self.B -= temp1*temp2
            self.updateGameInfo()
            self.updateTime()
            self.normalBack = f"执行成功，对A扣除{temp1},对B扣除{temp1*temp2}"
            self.nowOperatorIdx += 1
            self.nowOperatorIdx %= 2
            if self.A == 0 and self.B == 0:
                self.finish = True
                self.winner = playerID
                for qq in self.playerArr:
                    if qq != playerID:
                        self.scoreChangeList[qq] = -10
                    else:
                        self.scoreChangeList[qq] = 10
            return self.makeDict()
        if re.match("B [0-9]+ [0-9]+", Str) and self.state == "running":
            self.active = True
            if int(self.autoArgument[1]) == 0:
                self.legal = False
                self.errorBack = "你给定的值不合法，x应当为正整数"
                return self.makeDict()
            temp1 = int(self.autoArgument[1])
            temp2 = int(self.autoArgument[2])
            if temp1 > self.B or temp1*temp2 > self.A:
                self.legal = False
                self.errorBack = "你给定的值不合法，超出了所能挪动的数量"
                return self.makeDict()
            self.legal = True
            self.B -= temp1
            self.A -= temp1*temp2
            self.updateGameInfo()
            self.updateTime()
            self.normalBack = f"执行成功，对A扣除{temp1*temp2},对B扣除{temp1}"
            self.nowOperatorIdx += 1
            self.nowOperatorIdx %= 2
            if self.A == 0 and self.B == 0:
                self.finish = True
                self.winner = playerID
                for qq in self.playerArr:
                    if qq != playerID:
                        self.scoreChangeList[qq] = -10
                    else:
                        self.scoreChangeList[qq] = 10
            return self.makeDict()
        self.active = False
        return self.makeDict()


if __name__ == "__main__":
    T = MoveStone()
    T.running(1, "kong")
