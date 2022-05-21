import random
import re
import time

"""""
返回的Json应当包含元素：{"state" : "running/waiting", "nowOperator": playerID , "active":True/False, "legal":True/False,
            "errorBack":"Str", "finish":True/False, "winner":playerID, "gameInfo":"Str", "lastOperationTime": int
            "normalBack":"Str"}
"""""


class FightTheLandlord:
    pokerModel = {'3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, 'J': 0, 'Q': 0, 'K': 0,
                  'A': 0, '2': 0, '鬼': 0, '王': 0}
    pokerIdx = {'3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11,
                'A': 12, '2': 13, '鬼': 14, '王': 15}
    allPoker = ['3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7',
                '8', '8', '8', '8', '9', '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q',
                'K', 'K', 'K', 'K', 'A', 'A', 'A', 'A', '2', '2', '2', '2', '鬼', '王']

    def __init__(self):
        self.nowOperatorIdx = 0
        self.playerArr = []
        self.state = "waiting"
        self.legal = True
        self.base = 1
        self.errorBack = "None"
        self.normalBack = "None"
        self.finish = False
        self.winner = "None"
        self.active = False
        self.breakGame = False
        self.outPoker = False
        self.landlord = 0
        self.lastOperator = 0
        self.lastPokerClass = "None"
        self.winnerScore = 10
        self.playerPoker = {}
        self.scoreChangeList = {}
        self.randPoker = []
        self.wantLandlordList = []
        self.gameInfo = "None"
        self.autoArgument = None
        self.autoPokerClass = "None"
        self.lastPoker = {}
        self.autoPoker = {}
        self.lightPoker = {}
        self.landlordSendPokerTime = 0
        self.lastOperationTime = time.time()

    def sendPokers(self):
        tempPoker = self.allPoker.copy()
        for i in range(0, 54):
            j = random.randint(0, 53)
            temp = tempPoker[i]
            tempPoker[i] = tempPoker[j]
            tempPoker[j] = temp
        #   0~16 17~33 34~50 51~53
        self.randPoker = tempPoker.copy()
        self.playerPoker[self.playerArr[0]] = self.pokerModel.copy()
        self.playerPoker[self.playerArr[1]] = self.pokerModel.copy()
        self.playerPoker[self.playerArr[2]] = self.pokerModel.copy()
        for i in range(0, 17):
            self.playerPoker[self.playerArr[0]][tempPoker[i]] += 1
        for i in range(17, 34):
            self.playerPoker[self.playerArr[1]][tempPoker[i]] += 1
        for i in range(34, 51):
            self.playerPoker[self.playerArr[2]][tempPoker[i]] += 1

    def sendLandlordPokers(self):
        for i in range(51, 54):
            self.playerPoker[self.landlord][self.randPoker[i]] += 1

    def queryLightPoker(self, playerID):
        return self.lightPoker.get(playerID, False)

    def queryPokerInfo(self, playerID):
        # print(self.playerPoker[playerID])
        Str = ""
        for i in self.playerPoker[playerID]:
            num = self.playerPoker[playerID][i]
            for j in range(0, num):
                Str += f"[{i}]"
        return Str

    def queryLandlordPoker(self):
        Str = ""
        for i in range(51, 54):
            Str += f"[{self.randPoker[i]}]"
        return Str

    def getLandlord(self):
        return self.landlord

    def getLastOperationTime(self):
        return self.lastOperationTime

    def updateTime(self):
        self.lastOperationTime = time.time()

    def getNowOperator(self):
        if len(self.playerArr) < 3:
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
        if self.lastOperator == self.landlord:
            Str = f"当前对局信息:\n出牌人:[(地主){self.lastOperator}]\n出牌:\n"
        else:
            Str = f"当前对局信息:\n出牌人:[(平民){self.lastOperator}]\n出牌:\n"
        for i in self.lastPoker:
            num = self.lastPoker[i]
            for j in range(0, num):
                Str += f"[{i}]"
        Str += "\n剩余牌数:"
        for qq in self.playerArr:
            if qq == self.landlord:
                Str += f"\n[(地主){qq}]：{self.getPokerNumber(qq)}"
            else:
                Str += f"\n[(平民){qq}]：{self.getPokerNumber(qq)}"
        self.gameInfo = Str

    def getPokerNumber(self, playerID):
        res = 0
        for i in self.playerPoker.get(playerID, {}):
            res += self.playerPoker.get(playerID, {}).get(i, 0)
        return res

    def checkPokerLegal(self):
        if self.lastOperator == self.getNowOperator():
            if self.autoPokerClass == "王炸" or self.autoPokerClass == "炸弹":
                self.base *= 2
            return True
        if self.lastPokerClass == "王炸":
            return False
        if self.autoPokerClass == "王炸":
            self.base *= 2
            return True
        if self.autoPokerClass == "炸弹":
            if self.lastPokerClass != "炸弹":
                self.base *= 2
                return True
            val1 = 0
            val2 = 0
            for i in self.lastPoker:
                if self.lastPoker[i] == 4:
                    val1 += self.pokerIdx[i]
                    break
            for i in self.autoPoker:
                if self.autoPoker[i] == 4:
                    val2 += self.pokerIdx[i]
                    break
            if val2 > val1:
                self.base *= 2
                return True
            else:
                return False
        if self.lastPokerClass != self.autoPokerClass:
            return False
        val1 = 0
        val2 = 0
        if re.match("顺子.*", self.autoPokerClass):
            for i in self.lastPoker:
                if self.lastPoker[i] == 1:
                    val1 += self.pokerIdx[i]
                    break
            for i in self.autoPoker:
                if self.autoPoker[i] == 1:
                    val2 += self.pokerIdx[i]
                    break
            return val2 > val1
        if re.match("三.*", self.autoPokerClass):
            for i in self.lastPoker:
                if self.lastPoker[i] == 3:
                    val1 += self.pokerIdx[i]
                    break
            for i in self.autoPoker:
                if self.autoPoker[i] == 3:
                    val2 += self.pokerIdx[i]
                    break
            return val2 > val1
        if re.match("连对.*", self.autoPokerClass) or re.match("对子", self.autoPokerClass):
            for i in self.lastPoker:
                if self.lastPoker[i] == 2:
                    val1 += self.pokerIdx[i]
                    break
            for i in self.autoPoker:
                if self.autoPoker[i] == 2:
                    val2 += self.pokerIdx[i]
                    break
            return val2 > val1
        if re.match("四带二", self.autoPokerClass):
            for i in self.lastPoker:
                if self.lastPoker[i] == 4:
                    val1 += self.pokerIdx[i]
                    break
            for i in self.autoPoker:
                if self.autoPoker[i] == 4:
                    val2 += self.pokerIdx[i]
                    break
            return val2 > val1
        if re.match("单张", self.autoPokerClass):
            for i in self.lastPoker:
                if self.lastPoker[i] == 1:
                    val1 += self.pokerIdx[i]
                    break
            for i in self.autoPoker:
                if self.autoPoker[i] == 1:
                    val2 += self.pokerIdx[i]
                    break
            return val2 > val1
        return False

    def randThePlayer(self):
        for i in range(0, 3):
            idx = random.randint(0, 2)
            tempID = self.playerArr[idx]
            self.playerArr[idx] = self.playerArr[i]
            self.playerArr[i] = tempID

    def getPokerModel(self, Str):
        temp = self.pokerModel.copy()
        s = ""
        for c in Str:
            if s == "1":
                s += c
            else:
                s = c
            if s == "1":
                continue
            if self.pokerModel.get(s, -1) == -1:
                self.errorBack = f"试图出一张不存在的牌: {s}"
                self.autoPokerClass = "不合法"
                return
            temp[s] += 1
        if s == "1":
            self.errorBack = f"试图出一张不存在的牌: {s}"
            self.autoPokerClass = "不合法"
            return
        playerID = self.getNowOperator()
        for i in temp:
            if self.playerPoker[playerID][i] < temp[i]:
                self.autoPokerClass = "不合法"
                self.errorBack = f"试图出一张超出自己拥有数目的牌: {i}"
                return
        numDic = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for i in temp:
            numDic[temp[i]] += 1
        if numDic[1] == 2 and numDic[2] == 0 and numDic[3] == 0 and numDic[4] == 0:
            if temp['鬼'] == 1 and temp['王'] == 1:
                self.autoPokerClass = "王炸"
                self.autoPoker = temp.copy()
                return
            else:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
        if numDic[4]:
            if numDic[4] > 1 or numDic[3] != 0:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            if numDic[1] == 2 and numDic[2] == 0:
                self.autoPokerClass = "四带二单"
                self.autoPoker = temp.copy()
                return
            if numDic[1] == 0 and numDic[2] == 1:
                self.autoPokerClass = "四带二单"
                self.autoPoker = temp.copy()
                return
            if numDic[1] == 0 and numDic[2] == 2:
                self.autoPokerClass = "四带二双"
                self.autoPoker = temp.copy()
                return
            if numDic[1] == 0 and numDic[2] == 0:
                self.autoPokerClass = "炸弹"
                self.autoPoker = temp.copy()
                return
            else:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
        if numDic[1] >= 5 and numDic[2] == 0 and numDic[3] == 0 and numDic[4] == 0:
            Min = 17
            Max = 0
            for i in temp:
                if temp[i] != 0:
                    Min = min(Min, self.pokerIdx[i])
                    Max = max(Max, self.pokerIdx[i])
            if Max < 13 and (Max - Min + 1) == numDic[1]:
                self.autoPokerClass = f"顺子{numDic[1]}"
                self.autoPoker = temp.copy()
            else:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
            return
        if numDic[1] == 1 and numDic[2] == 0 and numDic[3] == 0 and numDic[4] == 0:
            self.autoPokerClass = "单张"
            self.autoPoker = temp.copy()
            return
        if numDic[1] == 0 and numDic[2] == 1 and numDic[3] == 0 and numDic[4] == 0:
            self.autoPokerClass = "对子"
            self.autoPoker = temp.copy()
            return
        if numDic[1] == 0 and numDic[2] >= 3 and numDic[3] == 0 and numDic[4] == 0:
            if temp['2'] == 2:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            Min = 17
            Max = 0
            for i in temp:
                if temp[i] == 2:
                    Min = min(Min, self.pokerIdx[i])
                    Max = max(Max, self.pokerIdx[i])
            self.autoPokerClass = f"连对{numDic[2]}"
            if (Max - Min + 1) != numDic[2]:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            self.autoPoker = temp.copy()
            return
        if numDic[1] == 0 and numDic[2] == 0 and numDic[3] != 0 and numDic[4] == 0:
            if temp['2'] == 3 and numDic[3] != 1:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            self.autoPokerClass = f"三顺{numDic[3]}"
            self.autoPoker = temp.copy()
            return
        if numDic[1] == numDic[3] and numDic[2] == 0 and numDic[3] != 0 and numDic[4] == 0:
            if temp['2'] == 3 and numDic[3] != 1:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            Min = 17
            Max = 0
            for i in temp:
                if temp[i] == 3:
                    Min = min(Min, self.pokerIdx[i])
                    Max = max(Max, self.pokerIdx[i])
            if (Max - Min + 1) != numDic[3]:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            self.autoPokerClass = f"三顺{numDic[3]}带单"
            self.autoPoker = temp.copy()
            return
        if numDic[2]*2 == numDic[3] and numDic[1] == 0 and numDic[3] != 0 and numDic[4] == 0:
            if temp['2'] == 3 and numDic[3] != 1:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            Min = 17
            Max = 0
            for i in temp:
                if temp[i] == 3:
                    Min = min(Min, self.pokerIdx[i])
                    Max = max(Max, self.pokerIdx[i])
            if (Max - Min + 1) != numDic[3]:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            self.autoPokerClass = f"三顺{numDic[3]}带单"
            self.autoPoker = temp.copy()
            return
        if numDic[1] == 0 and numDic[2] == numDic[3] and numDic[3] != 0 and numDic[4] == 0:
            if temp['2'] == 3 and numDic[3] != 1:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            Min = 17
            Max = 0
            for i in temp:
                if temp[i] == 3:
                    Min = min(Min, self.pokerIdx[i])
                    Max = max(Max, self.pokerIdx[i])
            if (Max - Min + 1) != numDic[3]:
                self.autoPokerClass = "不合法"
                self.errorBack = "无效的牌组"
                return
            self.autoPokerClass = f"三顺{numDic[3]}带双"
            self.autoPoker = temp.copy()
            return
        self.autoPokerClass = "不合法"
        self.errorBack = "无效的牌组"

    def checkEmpty(self, playerID):
        for i in self.playerPoker.get(playerID, {}):
            if self.playerPoker.get(playerID, {})[i] != 0:
                return False
        return True

    def makeDict(self):
        Dict = {"state": self.state, "nowOperator": self.getNowOperator(), "active": self.active,
                "legal": self.legal, "errorBack": self.errorBack, "normalBack": self.normalBack,
                "breakGame": self.breakGame, "playerArr": self.playerArr, "landlord": self.landlord,
                "finish": self.finish, "winner": self.winner, "scoreChangeList": self.scoreChangeList,
                "gameInfo": self.gameInfo, "lastOperationTime": self.lastOperationTime}
        return Dict

    def clearPoker(self):
        for i in self.playerPoker:
            self.playerPoker[i] = self.pokerModel.copy()

    def deletePoker(self, playerID, Dict):
        for i in Dict:
            self.playerPoker[playerID][i] -= Dict[i]

    def reset(self):
        self.nowOperatorIdx = 0
        self.playerArr = []
        self.state = "waiting"
        self.legal = True
        self.base = 1
        self.errorBack = "None"
        self.normalBack = "None"
        self.finish = False
        self.winner = "None"
        self.active = False
        self.breakGame = False
        self.outPoker = False
        self.landlord = 0
        self.lastOperator = 0
        self.lastPokerClass = "None"
        self.winnerScore = 10
        self.playerPoker = {}
        self.scoreChangeList = {}
        self.randPoker = []
        self.wantLandlordList = []
        self.gameInfo = "None"
        self.autoArgument = None
        self.autoPokerClass = "None"
        self.lastPoker = {}
        self.autoPoker = {}
        self.lightPoker = {}
        self.landlordSendPokerTime = 0
        self.lastOperationTime = time.time()

    def running(self, playerID, Str):
        self.updateArgument(Str)
        self.updateGameInfo()
        if re.match("斗地主掀桌", Str) and not(self.state == "waiting"):
            self.active = True
            if time.time() - self.lastOperationTime < 2 * 60:
                self.legal = False
                self.errorBack = "距离上一次合法操作未到2分钟，无法掀桌"
            else:
                self.legal = True
                self.breakGame = True
                for qq in self.playerArr:
                    if qq != self.getNowOperator():
                        self.scoreChangeList[qq] = +5*self.base
                    else:
                        self.scoreChangeList[qq] = -25*self.base
            return self.makeDict()
        if re.match("我牌呢", Str) and self.state != "waiting" and self.playerArr.count(playerID) != 0:
            self.active = True
            self.legal = False
            self.errorBack = "玩家查询牌信息，已将牌再次发送给玩家"
            return self.makeDict()
        if re.match("斗地主对局信息", Str):
            self.active = True
            self.legal = False
            self.errorBack = self.gameInfo
            if self.state != "对局中":
                self.errorBack = "还没开局，暂无信息"
            return self.makeDict()
        if re.match("离开斗地主", Str):
            self.active = True
            self.legal = False
            if self.playerArr.count(playerID) == 0:
                self.errorBack = "你没在里面呢..."
                return self.makeDict()
            if self.state != "waiting":
                self.errorBack = "对局已经开始了呢..."
                return self.makeDict()
            self.errorBack = "好的，你已离开"
            self.playerArr.remove(playerID)
            return self.makeDict()
        if re.match("加入斗地主", Str):
            self.active = True
            if self.state != "waiting":
                self.legal = False
                self.errorBack = "对局已经开始了，等待下一轮吧..."
            else:
                if self.playerArr.count(playerID) == 0:
                    self.legal = True
                    self.updateTime()
                    self.playerArr.append(playerID)
                    self.normalBack = f"加入成功！\n玩家列表:{self.playerArr}\n"
                    if len(self.playerArr) == 3:
                        self.state = "叫地主"
                        self.nowOperatorIdx = 0
                        self.normalBack = f"加入成功！\n玩家列表:{self.playerArr}\n人数已满，游戏开始！"
                        self.randThePlayer()
                        self.sendPokers()
                else:
                    self.legal = False
                    self.errorBack = "你已经在对局当中了"
            return self.makeDict()
        if re.match("明牌", Str) and self.playerArr.count(playerID) != 0 and not self.queryLightPoker(playerID)\
                and not self.outPoker and self.state != "waiting":
            self.active = True
            self.lightPoker[playerID] = True
            self.legal = False
            self.errorBack = "玩家明牌"
            self.base *= 2
            return self.makeDict()
        if self.getNowOperator() != playerID:
            self.active = False
            return self.makeDict()
        if re.match("叫地主", Str) and self.state == "叫地主":
            self.active = True
            self.updateTime()
            self.wantLandlordList.append(playerID)
            if len(self.wantLandlordList) > 1:
                self.base *= 2
            self.legal = False
            self.errorBack = "玩家叫地主"
            self.nowOperatorIdx += 1
            if self.nowOperatorIdx == 3:
                if len(self.wantLandlordList) == 0:
                    self.legal = False
                    self.nowOperatorIdx = 0
                    self.errorBack = "无人叫地主"
                    self.state = "叫地主"
                    self.clearPoker()
                    self.randThePlayer()
                    self.sendPokers()
                    self.base = 1
                else:
                    self.legal = False
                    self.errorBack = "叫地主结束"
                    self.state = "对局中"
                    idx = random.randint(0, len(self.wantLandlordList) - 1)
                    self.landlord = self.wantLandlordList[idx]
                    self.lastOperator = self.landlord
                    for i in range(0, 3):
                        if self.playerArr[i] == self.landlord:
                            self.nowOperatorIdx = i
                            break
                    self.sendLandlordPokers()
            return self.makeDict()
        if re.match("不叫", Str) and self.state == "叫地主":
            self.active = True
            self.legal = False
            self.updateTime()
            self.errorBack = "玩家不叫"
            self.nowOperatorIdx += 1
            if self.nowOperatorIdx == 3:
                if len(self.wantLandlordList) == 0:
                    self.legal = False
                    self.nowOperatorIdx = 0
                    self.errorBack = "无人叫地主"
                    self.state = "叫地主"
                    self.clearPoker()
                    self.sendPokers()
                    self.base = 1
                else:
                    self.legal = False
                    self.errorBack = "叫地主结束"
                    self.state = "对局中"
                    idx = random.randint(0, len(self.wantLandlordList) - 1)
                    self.landlord = self.wantLandlordList[idx]
                    self.lastOperator = self.landlord
                    for i in range(0, 3):
                        if self.playerArr[i] == self.landlord:
                            self.nowOperatorIdx = i
                            break
                    self.sendLandlordPokers()
            return self.makeDict()
        if re.match("过", Str) and self.state == "对局中":
            self.active = True
            if self.lastOperator == playerID:
                self.legal = False
                self.errorBack = "自己过自己的牌？"
            else:
                self.legal = True
                self.normalBack = "玩家过牌"
                self.nowOperatorIdx += 1
                self.nowOperatorIdx %= 3
                self.updateTime()
            return self.makeDict()
        if re.match("出 .*", Str) and self.state == "对局中":
            self.active = True
            self.getPokerModel(self.autoArgument[1])
            if self.autoPokerClass == "不合法":
                self.legal = False
                return self.makeDict()
            if not self.checkPokerLegal():
                self.legal = False
                self.errorBack = "牌好像对不上...或者没对方大"
                return self.makeDict()
            self.legal = True
            if self.landlord == playerID:
                self.landlordSendPokerTime += 1
            self.normalBack = "操作成功\n"
            self.outPoker = True
            self.lastPoker = self.autoPoker
            self.lastPokerClass = self.autoPokerClass
            self.lastOperator = playerID
            self.deletePoker(playerID, self.autoPoker)
            self.updateGameInfo()
            self.updateTime()
            self.normalBack += self.gameInfo
            self.nowOperatorIdx += 1
            self.nowOperatorIdx %= 3
            if self.checkEmpty(playerID):
                self.finish = True
                if self.landlord == playerID:
                    #   地主获胜
                    self.winner = "地主"
                    yu = 0
                    for qq in self.playerArr:
                        if qq != self.landlord:
                            yu += self.getPokerNumber(qq)
                    if yu == 34:
                        self.base *= 2
                    for qq in self.playerArr:
                        if qq == self.landlord:
                            self.scoreChangeList[qq] = 20*self.base
                        else:
                            self.scoreChangeList[qq] = -10*self.base
                else:
                    #   平民获胜
                    self.winner = "平民"
                    if self.landlordSendPokerTime <= 1:
                        self.base *= 2
                    for qq in self.playerArr:
                        if qq == self.landlord:
                            self.scoreChangeList[qq] = -20*self.base
                        else:
                            self.scoreChangeList[qq] = 10*self.base
            return self.makeDict()

        self.active = False
        return self.makeDict()


if __name__ == "__main__":
    T = FightTheLandlord()
    T.running(1, "kong")
