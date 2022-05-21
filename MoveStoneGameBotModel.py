import random
import re
import time

"""""
返回的Json应当包含元素：{"state" : "running/waiting", "nowOperator": playerID , "active":True/False, "legal":True/False,
            "errorBack":"Str", "finish":True/False, "winner":playerID, "gameInfo":"Str", "lastOperationTime": int
            "normalBack":"Str"}
"""""
"""""
for (int i = 0; i <= 1000; i++) {
        for (int j = 0; j <= 1000; j++) {
            if (ans[i][j] == false) {
                for (int k = 1; k + i <= 1000; k++) {
                    for (int s = 0; k * s + j <= 1000; s++) {
						if(!ans[i + k][j + s * k]){	
							ans[i + k][j + s * k] = true;
							from[i + k][j + s * k] = {'A', k, s};
						}
					}
                }
                for (int k = 1; k + j <= 1000; k++) {
                    for (int s = 0; s * k + i <= 1000; s++) {
						if(!ans[i + s * k][j + k]){
							ans[i + s * k][j + k] = true;
							from[i + s * k][j + k] = {'B', k, s};
						}
					}
                }
            }
        }
    }
"""""
Answer = {}
Sign = {}
for i in range(0, 1000):
    for j in range(0, 1000):
        if not Sign.get((i,j), False):
            for k in range(1, 1000-i):
                for s in range(0, int((1000 - j)/k)):
                    if not Sign.get((i+k,j+s*k)):
                        Sign[(i+k,j+s*k)] = True
                        Answer[(i+k,j+s*k)] = ('A', k, s)
            for k in range(1, 1000 - j):
                for s in range(0, int((1000 - i) / k)):
                    if not Sign.get((i + s*k, j + k)):
                        Sign[(i + s*k, j + k)] = True
                        Answer[(i + s*k, j + k)] = ('B', k, s)


class MoveStoneBotModel:
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
        if len(self.playerArr) == 0:
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

    def solveByBot(self, playerID):
        temp = Answer.get((self.A, self.B), ('A', 0, 0))
        # print(temp)
        if temp[1] == 0 and temp[2] == 0:
            #   没有最优解
            if self.A > self.B:
                x = random.randint(1, self.B)
                y = random.randint(0, int(self.A/x))
                self.normalBack += f"\n\n机器选择执行: B {x} {y}\n对A扣除{x*y},对B扣除{x}"
                self.A -= x*y
                self.B -= x
            else:
                x = random.randint(1, self.A)
                y = random.randint(0, int(self.B / x))
                self.normalBack += f"\n\n机器选择执行: A {x} {y}\n对A扣除{x},对B扣除{x*y}"
                self.A -= x
                self.B -= x*y
        else:
            #   有最优解
            self.normalBack += f"\n\n机器选择执行: {temp[0]} {temp[1]} {temp[2]}"
            if temp[0] == 'A':
                self.A -= temp[1]
                self.B -= temp[1]*temp[2]
                self.normalBack += f"\n对A扣除{temp[1]},对B扣除{temp[1]*temp[2]}"
            else:
                self.B -= temp[1]
                self.A -= temp[1]*temp[2]
                self.normalBack += f"\n对A扣除{temp[1]*temp[2]},对B扣除{temp[1]}"
        if self.A == 0 and self.B == 0:
            self.finish = True
            self.winner = 1784518480
            self.scoreChangeList = {1784518480: 10, playerID: -10}

    def running(self, playerID, Str):
        self.updateArgument(Str)
        self.updateGameInfo()
        if re.match("人机挪石头投降", Str) and self.state == "running":
            self.active = True
            self.legal = False
            if self.playerArr.count(playerID) == 0:
                self.errorBack = "你没开始游戏呢..."
            else:
                self.winner = 1784518480
                self.scoreChangeList[self.winner] = 10 - int((self.A + self.B) / 200)
                self.scoreChangeList[playerID] = int((self.A + self.B) / 200) - 10
                self.finish = True
                self.legal = True
                self.normalBack = "你选择了投降"
            return self.makeDict()
        if re.match("人机挪石头对局信息", Str):
            self.active = True
            self.legal = False
            self.errorBack = self.gameInfo
            if self.state == "waiting":
                self.errorBack = "还没开局，暂无信息"
            return self.makeDict()
        if re.match("开始人机挪石头", Str):
            self.active = True
            if self.state == "running":
                self.active = False
                self.legal = False
                self.errorBack = "你已经开始人机挪石头了..."
            else:
                self.legal = True
                self.active = True
                self.updateTime()
                self.playerArr.append(playerID)
                self.nowOperatorIdx = 0
                self.normalBack = f"人机对局开始！祝您好运！\n"
                self.state = "running"
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
            self.nowOperatorIdx %= 1
            if self.A == 0 and self.B == 0:
                self.finish = True
                self.winner = playerID
                for qq in self.playerArr:
                    if qq != playerID:
                        self.scoreChangeList[qq] = -10
                    else:
                        self.scoreChangeList[qq] = 10
                self.scoreChangeList[1784518480] = -10
                return self.makeDict()
            else:
                self.solveByBot(playerID)
                self.updateGameInfo()
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
            self.nowOperatorIdx %= 1
            if self.A == 0 and self.B == 0:
                self.finish = True
                self.winner = playerID
                for qq in self.playerArr:
                    if qq != playerID:
                        self.scoreChangeList[qq] = -10
                    else:
                        self.scoreChangeList[qq] = 10
                self.scoreChangeList[1784518480] = -10
                return self.makeDict()
            else:
                self.solveByBot(playerID)
                self.updateGameInfo()
            return self.makeDict()
        self.active = False
        return self.makeDict()


if __name__ == "__main__":
    T = MoveStoneBotModel()
    T.running(1, "kong")
