# -*- coding: utf-8 -*-
import miraicle
import json
import re
import random
import time


class Bot:
    st = time.strftime("%H:%M:%S", time.localtime())
    owner = 1924645279
    adminPath = '.\\Data\\admin.txt'
    admin = {}
    userScorePath = '.\\Data\\userScore.txt'
    userScore = {}
    msgMatchPath = '.\\Data\\msgMatch.txt'
    msgMatch = {}
    namePath = '.\\Data\\name.txt'
    name = {}
    teaRoomStatePath = '.\\Data\\teaRoomState.txt'
    teaRoomState = {}
    teaRoomAutoStatePath = '.\\Data\\teaRoomAutoState.txt'
    teaRoomAutoState = {}
    time_hour = time.strftime('%H', time.localtime())
    #   记录斗地主数据,建立映射<GroupNumber, 斗地主类实例引用>
    douDiZhuGroupData = {}
    #   <QQNumber , ...>
    douDiZhuAccountData = {}

    def __init__(self):
        self.autoBot = None
        self.autoGroupNumber = None
        self.autoFriendNumber = None
        self.autoPlain = None
        self.autoMsgJson = None
        self.autoName = None
        self.autoArguments = []
        self.autoImage = None
        self.isFriend = False
        with open(self.userScorePath, 'r') as f:
            self.userScore = json.load(f)
        with open(self.msgMatchPath, 'r') as f:
            self.msgMatch = json.load(f)
        with open(self.adminPath, 'r') as f:
            self.admin = json.load(f)
        with open(self.namePath, 'r') as f:
            self.name = json.load(f)
        with open(self.teaRoomStatePath, 'r') as f:
            self.teaRoomState = json.load(f)
        with open(self.teaRoomAutoStatePath, 'r') as f:
            self.teaRoomAutoState = json.load(f)
        self.time_hour = time.strftime('%H', time.localtime())

    def douDiZhuSystem(self):
        if self.autoPlain == "斗地主":
            self.output("玩家需要添加机器人为好友才可正常使用...\n斗地主————经典玩法。\n话不多说，赶紧发送[加入斗地主]和伙伴们开一局吧！\n\n斗地主————反常玩法:\n\
                   玩法与经典玩法大同小异，不同之处为：经典玩法每轮都是出比之前更大的牌，而反常玩法则是交替更改这个大小要求，我们简称其为'逆序状态'。\n\
                   比如本轮，你要出比对方大的牌，而下一轮，你则要出比对方小的牌。\n\
                   但是呢，对所有人来说，炸弹都是能炸非炸弹的，王炸都是能炸炸弹或非炸弹的，该规则固定不变。\n地主先发牌，平民在第一轮时逆序状态为'否'，即正常出牌。\n\
                   赶紧发送[加入反常斗地主]和伙伴们开一局吧！")
        if self.douDiZhuGroupData.get(self.autoGroupNumber, None) is None:
            self.douDiZhuGroupData[self.autoGroupNumber] = DouDiZhu()
        self.douDiZhuGroupData[self.autoGroupNumber].running()

    def clearTeaRoomState(self, bot: miraicle.Mirai):
        self.updateTime()
        self.autoBot = bot
        self.autoFriendNumber = 1784518480
        self.sentTeaRoomMessage("[茶馆已闭馆]这位客官，此刻入夜已深，尽早歇息去罢。\n若仍要在茶馆落脚，可再次发送[进入茶馆]。")
        for qq in self.teaRoomState:
            if qq == 'online':
                self.teaRoomState[qq] = 0
            else:
                self.teaRoomState[qq] = False
        self.update()

    def solveGroupMessage(self, bot: miraicle.Mirai, msg: miraicle.GroupMessage):  #
        self.autoArguments = msg.plain.split(' ')
        self.isFriend = False
        self.autoBot = bot
        self.autoGroupNumber = msg.group
        self.autoPlain = msg.plain
        self.autoMsgJson = msg.json
        self.autoImage = msg.first_image
        self.autoFriendNumber = msg.sender
        self.autoName = msg.sender_name
        self.messageMatchReply()
        self.douDiZhuSystem()
        self.update()

    def solveFriendMessage(self, bot: miraicle.Mirai, msg: miraicle.FriendMessage):
        self.autoArguments = msg.plain.split()  # 默认以单个空格作为分隔符 ----- by Liedou
        self.isFriend = True
        self.autoBot = bot
        self.autoPlain = msg.plain
        self.autoMsgJson = msg.json
        self.autoImage = msg.first_image
        self.autoFriendNumber = msg.sender
        self.autoName = msg.sender_name
        self.messageMatchReply()
        self.update()

    def messageMatchReply(self):
        text = self.msgMatch.get(self.autoPlain, "-1")
        if self.autoPlain == "开启便捷茶馆":
            self.output("好的", True)
            self.setTeaRoomAutoState(self.autoFriendNumber, True)
            return
        if self.autoPlain == "关闭便捷茶馆":
            self.output("好的", True)
            self.setTeaRoomAutoState(self.autoFriendNumber, False)
            return
        if re.match("添加问答 .* .*", self.autoPlain) is not None:
            if not self.isAdmin(self.autoFriendNumber):
                self.output("你不是管理员！", True)
            else:
                self.msgMatch[self.autoArguments[1]] = self.autoArguments[2]
                self.output("好的", True)
            return
        if re.match("添加管理员 [0-9]+", self.autoPlain) is not None:
            if self.autoFriendNumber != self.owner:
                self.output("你不是墨晓晓！", True)
            else:
                self.output("好的", True)
                self.addAdministrator(int(self.autoArguments[1]))
            return
        if re.match("删除管理员 [0-9]+", self.autoPlain) is not None:
            if self.autoFriendNumber != self.owner:
                self.output("你不是墨晓晓！", True)
            else:
                self.output("好的", True)
                self.deleteAdministrator(int(self.autoArguments[1]))
            return
        if re.match("打印数据信息", self.autoPlain) is not None:
            self.outputAllData()
            self.output("好的", True)
            return
        if re.match("设置昵称 .*", self.autoPlain) is not None:
            if len(self.autoArguments[1]) <= 20:
                self.output("好的", True)
                self.setName(self.autoArguments[1])
            else:
                self.output("不行，你昵称太长了", True)
            return
        if re.match("传句话给 [0-9]+ .*", self.autoPlain) is not None:
            self.output("行叭我试试，如果我和TA不是好友那就没办法了哦", True)
            Str = ""
            for i in self.autoArguments[2:]:
                Str += i
                Str += ' '
            self.sentMessage(int(self.autoArguments[1]), Str)
            return
        if re.match("茶馆 .*", self.autoPlain) is not None:
            self.updateTime()
            if self.getTeaState(self.autoFriendNumber):
                if not self.isFriend:
                    self.output(f"[online:{self.getTeaRoomPeopleNumber()}]好嘞，小的这就帮您转达", True)
                Str = ""
                for i in self.autoArguments[1:]:
                    Str += i
                    Str += ' '
                if self.autoImage is not None:
                    Str += f"[mirai:image:{self.autoImage.image_id}]"
                self.sentTeaRoomMessage(Str)
            else:
                self.output("您这不还没进茶馆嘛...", True)
            return
        if re.match("反馈 .*", self.autoPlain) is not None:
            Str = ""
            for i in self.autoArguments[1:]:
                Str += i
                Str += ' '
            self.output("您的反馈已发送到开发组，感谢您的宝贵建议", True)
            self.sentFeedBackMessage(f"收到一条反馈信息:\n{Str}")
            return
        if self.autoPlain == "茶馆在线列表":
            self.output(self.queryTeaRoomOnlineList())
            return
        if self.autoPlain == "菜单":
            self.showMenu()
            return
        if self.autoPlain == "进入茶馆":
            if self.getTeaState(self.autoFriendNumber):
                self.output("客官您已经在茶馆里了", True)
            else:
                self.output("好的", True)
                self.setTeaRoomState(True)
                self.output(f"当前在线人数:{self.getTeaRoomPeopleNumber()}")
            return
        if self.autoPlain == "离开茶馆":
            if self.getTeaState(self.autoFriendNumber):
                self.output("好的", True)
                self.setTeaRoomState(False)
            else:
                self.output("客官您本就不在茶馆之中", True)
            return
        if not self.isFriend:
            if re.match("禁言 [0-9]+ [0-9]+", self.autoPlain):
                if not self.isAdmin(self.autoFriendNumber):
                    self.output("你掺和啥呢..")
                else:
                    if not (self.autoBot.is_self.owner(self.robotQQ, self.autoGroupNumber) or self.autoBot.is_administrator(self.robotQQ,
                                                                                                   self.autoGroupNumber)):
                        self.output("啊这,我...我做不到啊")
                    else:
                        if self.isAdmin(self.autoFriendNumber):
                            if self.autoBot.is_self.owner(self.autoArguments[1], self.autoGroupNumber) or self.autoBot.is_administrator(
                                    self.autoArguments[1], self.autoGroupNumber):
                                self.output("您是拿我寻开心是吗？")
                            else:
                                self.output("好的")
                                self.autoBot.mute(self.autoGroupNumber, int(self.autoArguments[1]), int(self.autoArguments[2]) * 60)
                return
            if re.match("解除禁言 [0-9]+", self.autoPlain):
                if not self.isAdmin(self.autoFriendNumber):
                    self.output("你掺和啥呢..")
                else:
                    if not (self.autoBot.is_self.owner(self.robotQQ, self.autoGroupNumber) or self.autoBot.is_administrator(self.robotQQ,
                                                                                                   self.autoGroupNumber)):
                        self.output("啊这,我...我做不到啊")
                    else:
                        if self.isAdmin(self.autoFriendNumber):
                            if self.autoBot.is_self.owner(self.autoArguments[1], self.autoGroupNumber) or self.autoBot.is_administrator(
                                    self.autoArguments[1], self.autoGroupNumber):
                                self.output("您是拿我寻开心是吗？")
                            else:
                                self.output("好的")
                                self.autoBot.unmute(self.autoGroupNumber, self.autoArguments[1])
                return
            if re.match("踢出 [0-9]+", self.autoPlain):
                if not self.isAdmin(self.autoFriendNumber):
                    self.output("你掺和啥呢..")
                else:
                    if not (self.autoBot.is_self.owner(self.robotQQ, self.autoGroupNumber) or self.autoBot.is_administrator(self.robotQQ,
                                                                                                   self.autoGroupNumber)):
                        self.output("啊这,我...我做不到啊")
                    else:
                        if self.isAdmin(self.autoFriendNumber):
                            if self.autoBot.is_self.owner(self.autoArguments[1], self.autoGroupNumber) or self.autoBot.is_administrator(
                                    self.autoArguments[1], self.autoGroupNumber):
                                self.output("您是拿我寻开心是吗？")
                            else:
                                self.output("好的")
                                self.autoBot.kick(self.autoGroupNumber, self.autoArguments[1])
                return
            if self.autoPlain == "全体禁言":
                if not self.isAdmin(self.autoFriendNumber):
                    self.output("你掺和啥呢..")
                else:
                    if not (self.autoBot.is_self.owner(self.robotQQ, self.autoGroupNumber) or self.autoBot.is_administrator(self.robotQQ,
                                                                                                   self.autoGroupNumber)):
                        self.output("啊这,我...我做不到啊")
                    else:
                        self.autoBot.mute_all(self.autoGroupNumber)
                        self.output("好的")
                return
            if self.autoPlain == "解除全体禁言":
                if not self.isAdmin(self.autoFriendNumber):
                    self.output("你掺和啥呢..")
                else:
                    if not (self.autoBot.is_self.owner(self.robotQQ, self.autoGroupNumber) or self.autoBot.is_administrator(self.robotQQ,
                                                                                                   self.autoGroupNumber)):
                        self.output("啊这,我...我做不到啊")
                    else:
                        self.autoBot.unmute_all(self.autoGroupNumber)
                        self.output("好的")
                return
        if self.autoPlain == "个人信息":
            self.queryPersonalInformation()
            return
        if self.autoPlain == "设置昵称":
            self.showSetPersonalNick()
            return
        if self.autoPlain == "茶馆系统":
            self.showTeaRoomSystem()
            return
        if self.autoPlain == "群管系统":
            self.showGroupRegulateSystem()
            return
        if self.autoPlain == "娱乐系统":
            self.showRecreationSystem()
            return
        if self.autoPlain == "反馈系统":
            self.showFeedBackSystem()
            return
        if self.isFriend and self.getTeaRoomAutoState(self.autoFriendNumber):
            self.updateTime()
            if self.getTeaState(self.autoFriendNumber):
                self.sentTeaRoomMessage(self.getFullMsgInfo())
            return
        if text != "-1":
            self.output(text)
            return

    #   发送反馈信息到开发组群
    def sentFeedBackMessage(self, Str):
        self.autoBot.send_group_msg(
            261925581,
            Str
        )
        if self.autoImage is not None:
            self.autoBot.send_group_msg(
                261925581,
                msg=[
                    miraicle.Image.from_id(self.autoImage.image_id)
                ]
            )

    def showFeedBackSystem(self):
        Str = "\
    反馈系统是一项用于向机器人开发组反馈意见的功能。\n\
    如果使用者在使用机器人的过程中发现了程序的一些错误,\n\
    或者是有什么想法以及改进建议，都可以通过反馈系统将\n\
    建议发送到机器人开发组。并且反馈是匿名的。这意味着开发人员不会看到有关于您的个人信息\n\
    指令如下:\n\
    [反馈 内容]\n\
    注：你可以附带一张图片放在内容末端，图片将会发送到开发组"
        self.output(Str)

    def showRecreationSystem(self):
        Str = "-----娱 乐 系 统------\n\
    -------斗地主-------\n\
    ------等待开发------"
        self.output(Str)

    def showGroupRegulateSystem(self):
        Str = "\
    群管系统是一项便捷辅助进行对群员执行操作的功能,\
    本功能的使用前提是机器人在所在群拥有管理员权限。\
    并且使用者需是机器人的管理人员\n\
    具有如下指令:\n\
    [禁言 [qq] [时间:单位分钟]]\n\
    [解除禁言 [qq]]\n\
    [全体禁言]\n\
    [解除全体禁言]\n\
    [踢出 [qq]]"
        self.output(Str)

    def showSetPersonalNick(self):
        self.output("请通过回复'设置昵称 新昵称'来更改你的昵称")

    def showTeaRoomSystem(self):
        Str = f"\
    茶馆系统是一个聊天系统\n\
    使用者需要添加机器人为好友，然后发送[进入茶馆]或者[离开茶馆]\
    来改变自己的茶馆状态。\n\
    在你进入茶馆之后，你可以通过发送[茶馆 内容]来将你的内容发送到茶馆里\
    的所有客官当中。当然，这会暴露你所设置的个人昵称以及你的QQ号。\
    当然，别人在茶馆发言时，你也会接收到来自他们的消息。\n\
    你可以发送[茶馆在线列表]来查看此刻有多少人在茶馆中。\n\
    除此之外，你可以发送[开启/关闭便捷茶馆]来切换便捷模式，在该模式下，你私聊机器人时不需要发送[茶馆]前缀，消息也会被识别为茶馆消息\n\
    总结一下，就是五条指令:\n\
    [进入茶馆]\n\
    [离开茶馆]\n\
    [茶馆 内容]\n\
    [开启便捷茶馆]\n\
    [关闭便捷茶馆]\n\
    [茶馆在线列表]\n\
    注:关闭便捷模式情况下你可以附带一张图片在消息末端，但是你所发的QQ表情将会无效\n\
    而在便捷模式情况下，你所发的任QQ表情和图片都会严格按照原本的顺序和数目发送出去\n\
    祝您使用愉快。"
        self.output(Str)

    def getPersonalScore(self,number):
        return self.userScore.get(str(number), 0)

    def addPersonalScore(self, number, cnt):
        self.userScore[str(number)] = self.getPersonalScore(number) + cnt

    def queryPersonalInformation(self):
        Str = f"\
    --------个人信息--------\n\
    QQ:{self.autoFriendNumber}\n\
    昵称:{self.getName(self.autoFriendNumber)}\n\
    是否为管理员:{self.isAdmin(self.autoFriendNumber)}\n\
    茶馆状态:{self.getTeaState(self.autoFriendNumber)}\n\
    茶馆便捷状态:{self.getTeaRoomAutoState(self.autoFriendNumber)}\n\
    个人积分:{self.getPersonalScore(self.autoFriendNumber)}"
        self.output(Str, True)

    def queryTeaRoomOnlineList(self):
        Str = f"在线人数:{self.getTeaRoomPeopleNumber()}"
        for qq in self.teaRoomState:
            if qq != 'online' and self.teaRoomState.get(qq):
                Str += f"\n【{self.getName(qq)}({qq})】"
        return Str

    def showMenu(self):
        menu = "\
    ------- 菜 单 -------\n\
    ------个人信息------\n\
    ------设置昵称------\n\
    ------茶馆系统------\n\
    ------娱乐系统------\n\
    ------群管系统------\n\
    ------反馈系统------"
        self.output(menu)

    def getTeaState(self, number):
        return self.teaRoomState.get(str(number), False)

    def sentTeaRoomMessage(self, Str):
        for qq in self.teaRoomState:
            if self.getTeaState(qq) and qq != "online":
                self.autoBot.send_friend_msg(
                    int(qq),
                    msg=[
                        miraicle.Plain(
                            f"[online:{self.getTeaRoomPeopleNumber()}]茶馆[{self.st}]\n来自【{self.getName(self.autoFriendNumber)}(QQ:{self.autoFriendNumber})】的信息：\n"),
                        miraicle.MiraiCode(Str),
                    ]
                )

    #   发送私人消息Str到QQNumber
    def sentMessage(self, number, Str):
        self.autoBot.send_friend_msg(
            int(number),
            msg=[
                miraicle.Plain(f"[{self.st}]\n来自【{self.getName(self.autoFriendNumber)}】的信息：\n"),
                miraicle.Plain(Str),
            ]
        )

    def setTeaRoomState(self, state):
        self.teaRoomState[str(self.autoFriendNumber)] = state
        if state:
            self.teaRoomState["online"] = self.getTeaRoomPeopleNumber() + 1
        else:
            self.teaRoomState["online"] = self.getTeaRoomPeopleNumber() - 1

    def getTeaRoomPeopleNumber(self):
        return self.teaRoomState.get("online", 0)

    #   获取用户在机器人程序中的昵称
    def getName(self, number: str):
        return self.name.get(str(number), "无名氏")

    #   设置用户在机器人程序中的昵称
    def setName(self, Str):
        self.name[str(self.autoFriendNumber)] = Str

    #   判断发言人是不是机器人的管理员
    def isAdmin(self, number):
        return self.admin.get(str(number), False)

    def updateTime(self):
        self.st = time.strftime("%H:%M:%S", time.localtime())

    #   回复信息
    def output(self, Str, needAt=False):
        if not self.isFriend:
            if needAt:
                self.autoBot.send_group_msg(
                    self.autoGroupNumber,
                    msg=[
                        miraicle.At(self.autoFriendNumber),
                        miraicle.Plain("\n"),
                        miraicle.Plain(f"{Str}")
                    ]
                )
            else:
                self.autoBot.send_group_msg(
                    self.autoGroupNumber,
                    msg=[
                        miraicle.Plain(f"{Str}")
                    ]
                )
        else:
            self.autoBot.send_friend_msg(
                self.autoFriendNumber,
                Str
            )

    def outputAllData(self):
        for i in self.admin:
            print(i, type(i), self.admin.get(i), type(self.admin.get(i)))

        for i in self.userScore:
            print(i, type(i), self.admin.get(i), type(self.admin.get(i)))

        for i in self.admin:
            print(i, type(i), self.admin.get(i), type(self.admin.get(i)))

        for i in self.name:
            print(i, type(i), self.admin.get(i), type(self.admin.get(i)))

        print(self.autoName)

    def getFullMsgInfo(self):
        Str = ""
        msgChain = self.autoMsgJson.get('messageChain', None)
        for dic in msgChain:
            if dic.get('type', None) == 'Plain':
                Str += dic.get('text', None)
                continue
            if dic.get('type', None) == 'Face':
                Str += f"[mirai:face:{dic.get('faceId', 0)}]"
                continue
            if dic.get('type', None) == 'Image':
                Str += f"[mirai:image:{dic.get('imageId', 0)}]"
                continue
        return Str

    def addAdministrator(self, number):
        self.admin[str(number)] = True

    def deleteAdministrator(self, number):
        self.admin[str(number)] = False

    def addMsgMatch(self, Str1, Str2):
        self.msgMatch[Str1] = Str2

    def setTeaRoomAutoState(self, number, sign):
        self.teaRoomAutoState[str(number)] = sign

    def getTeaRoomAutoState(self, number):
        return self.teaRoomAutoState.get(str(number), False)

    def update(self):
        self.autoImage = None
        if self.getName(self.autoFriendNumber) == "无名氏":
            self.setName(self.autoName)
        with open(self.userScorePath, 'w') as f:
            f.write(json.dumps(self.userScore))
        with open(self.msgMatchPath, 'w') as f:
            f.write(json.dumps(self.msgMatch))
        with open(self.adminPath, 'w') as f:
            f.write(json.dumps(self.admin))
        with open(self.namePath, 'w') as f:
            f.write(json.dumps(self.name))
        with open(self.teaRoomStatePath, 'w') as f:
            f.write(json.dumps(self.teaRoomState))
        with open(self.teaRoomAutoStatePath, 'w') as f:
            f.write(json.dumps(self.teaRoomAutoState))

    robotQQ = 1784518480
    port = 8080
    verify_code = '114514'
    bot = miraicle.Mirai(robotQQ, verify_code, port)  # adapter='ws' 参数更改 websocket/http
    bot.run()


class DouDiZhu(Bot):
    allPokers = ['3', '3', '3', '3', '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', '7', '7', '7', '7',
                 '8', '8', '8', '8', '9'
        , '9', '9', '9', '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K', 'A',
                 'A',
                 'A', 'A', '2', '2', '2', '2', '鬼', '王']
    pokerModel = {'3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, 'J': 0, 'Q': 0, 'K': 0, 'A': 0,
                  '2': 0, '鬼': 0, '王': 0}
    pokerLevel = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11,
                  '2': 12, '鬼': 13, '王': 14}
    levelPoker = {0: '3', 1: '4', 2: '5', 3: '6', 4: '7', 5: '8', 6: '9', 7: '10', 8: 'J', 9: 'Q', 10: 'K', 11: 'A',
                  12: '2', 13: '鬼', 14: '王'}

    def init(self):
        self.numbersQQ = []
        self.landLord = None
        self.reserveLandLord = []
        self.poker = [{}, {}, {}]
        self.itsLess = [False, False, False]
        self.index = {}
        self.nowNumber = 0
        self.nowState = "等待玩家"
        self.nowPlayer = 0
        self.lastModel = "空"
        self.lastPoker = {}
        self.autoPoker = {}
        self.autoModel = "空"
        self.lastIndex = 0
        self.playModel = "空"
        self.poker[0] = self.pokerModel.copy()
        self.poker[1] = self.pokerModel.copy()
        self.poker[2] = self.pokerModel.copy()
        #   洗牌
        self.swapPoker(random.randint(0, 40), 52)
        self.swapPoker(random.randint(0, 40), 53)
        for i in range(100000):
            self.swapPoker(random.randint(0, 53), random.randint(0, 53))
        #   发牌
        for i in range(0, 51):
            pok = self.allPokers[i]
            self.poker[i % 3][pok] = self.poker[i % 3][pok] + 1

    def __init__(self):
        super().__init__()
        self.playModel = "空"
        self.numbersQQ = []
        self.landLord = None
        self.reserveLandLord = []
        self.poker = [{}, {}, {}]
        self.itsLess = [False, False, False]
        self.index = {}
        self.nowNumber = 0
        self.nowState = "等待玩家"
        self.nowPlayer = 0
        self.lastModel = "空"
        self.lastPoker = {}
        self.autoPoker = {}
        self.autoModel = "空"
        self.lastIndex = 0
        self.init()

    #   询问玩家牌信息
    def queryPoker(self, number) -> str:
        index = self.index[number]
        Str = ""
        for key in self.poker[index]:
            for val in range(0, self.poker[index][key]):
                Str = Str + '[' + key + ']'
        return Str

    def swapPoker(self, idx1, idx2):
        pok1 = self.allPokers[idx1]
        pok2 = self.allPokers[idx2]
        self.allPokers[idx1] = pok2
        self.allPokers[idx2] = pok1

    def addPlayer(self, number):
        self.numbersQQ.append(number)
        self.index[number] = self.nowNumber
        self.nowNumber += 1

    def compare(self, Less):
        if self.autoModel == "不合法":
            return False
        if self.lastModel == "空":
            return True
        if self.autoModel == "王炸":
            return True
        if self.lastModel != "炸弹" and self.lastModel != "王炸" and self.autoModel == "炸弹":
            return True
        if self.autoModel != self.lastModel:
            return False
        if self.autoModel == "炸弹":
            res1 = 0
            res2 = 0
            for i in self.lastPoker:
                res1 = self.getLevel(i)
            for i in self.autoPoker:
                res2 = self.getLevel(i)

            self.output(f"上一次牌的权值为：{res1}\n你的牌的权值为:{res2}")
            if Less:
                return res2 < res1
            else:
                return res2 > res1
        if self.autoModel == "四带二":
            res1 = 0
            res2 = 0
            for i in self.lastPoker:
                if self.lastPoker.get(i) == 4:
                    res1 = self.getLevel(i)
            for i in self.autoPoker:
                if self.autoPoker.get(i) == 4:
                    res2 = self.getLevel(i)

            self.output(f"上一次牌的权值为：{res1}\n你的牌的权值为:{res2}")
            if Less:
                return res2 < res1
            else:
                return res2 > res1
        if re.match("三顺.*", self.autoModel):
            res1 = 0
            res2 = 0
            for i in self.lastPoker:
                if self.lastPoker.get(i) == 3:
                    res1 += self.getLevel(i)
            for i in self.autoPoker:
                if self.autoPoker.get(i) == 3:
                    res2 += self.getLevel(i)

            self.output(f"上一次牌的权值为：{res1}\n你的牌的权值为:{res2}")
            if Less:
                return res2 < res1
            else:
                return res2 > res1
        if re.match("连对.*", self.autoModel) or self.autoModel == "对子":
            res1 = 0
            res2 = 0
            for i in self.lastPoker:
                if self.lastPoker.get(i) == 2:
                    res1 += self.getLevel(i)
            for i in self.autoPoker:
                if self.autoPoker.get(i) == 2:
                    res2 += self.getLevel(i)
            self.output(f"上一次牌的权值为：{res1}\n你的牌的权值为:{res2}")
            if Less:
                return res2 < res1
            else:
                return res2 > res1
        if re.match("顺子.*", self.autoModel) or self.autoModel == "单张":
            res1 = 0
            res2 = 0
            for i in self.lastPoker:
                if self.lastPoker.get(i) == 1:
                    res1 += self.getLevel(i)
            for i in self.autoPoker:
                if self.autoPoker.get(i) == 1:
                    res2 += self.getLevel(i)

            self.output(f"上一次牌的权值为：{res1}\n你的牌的权值为:{res2}")
            if Less:
                return res2 < res1
            else:
                return res2 > res1

    def checkPoker(self, number, msg):
        # index = self.getIndex(number, -1)
        need = {}
        s = ""
        tempDict = {}
        for i in msg:
            if s == "1":
                s += i
            else:
                s = i
            if s == '1':
                continue
            if self.getLevel(s) == -1:
                self.output(f"试图出一张不存在的牌:{s}")
                return "不合法"
            tempDict[self.getLevel(s)] = tempDict.get(self.getLevel(s), 0) + 1
            if tempDict[self.getLevel(s)] > self.getPokerNumber(number, s):
                self.output(f"试图出超过自己拥有数目的牌:{s}")
                return "不合法"
        for i in range(0, 15):
            if tempDict.get(i, 0) != 0:
                need[self.getPoker(i)] = tempDict.get(i, 0)
        self.autoPoker = need.copy()
        itsModel = "未知"
        if need.get('鬼', 0) > 0 and need.get('王', 0) > 0:
            itsModel = "假定王炸"
        if itsModel == "假定王炸":
            need['鬼'] = need.get('鬼') - 1
            need['王'] = need.get('王') - 1
            for i in need:
                if need.get(i) != 0:
                    self.output("或许是这对王带孩子来的...")
                    return "不合法"
            return "王炸"
        itsCount = {}
        for i in need:
            itsCount[need[i]] = itsCount.get(need[i], 0) + 1
        if itsCount.get(4, 0) == 1 and itsCount.get(1, 0) == 0 and itsCount.get(2, 0) == 0 and itsCount.get(3,
                                                                                                            0) == 0:
            return "炸弹"
        if itsCount.get(1, 0) == 0 and itsCount.get(2, 0) == 2 and itsCount.get(3, 0) == 0 and itsCount.get(4,
                                                                                                            0) == 1:
            return "四带二对"
        if itsCount.get(1, 0) == 2 and itsCount.get(2, 0) == 0 and itsCount.get(3, 0) == 0 and itsCount.get(4,
                                                                                                            0) == 1:
            return "四带二单"
        if itsCount.get(3, 0) != 0 and itsCount.get(4, 0) == 0:
            firstPokerLevel = None
            for i in need:
                if need.get(i) == 3:
                    firstPokerLevel = self.getLevel(i)
                    break
            for i in range(0, itsCount.get(3, 0)):
                if need.get(self.getPoker(firstPokerLevel + i), 0) != 3 or (
                        itsCount.get(3, 0) != 1 and i + firstPokerLevel == self.getLevel('2')):
                    self.output(f"试图出顺子、飞机或者三带，但是不连续或者把2给拿进去了...")
                    return "不合法"
            if itsCount.get(1, 0) == 0 and itsCount.get(2, 0) == 0:
                return f"三顺{itsCount.get(3, 0)}"
            if itsCount.get(1, 0) != 0 and itsCount.get(2, 0) != 0:
                self.output("试图三带单的同时还带双")
                return "不合法"
            if itsCount.get(1, 0) != 0:
                if itsCount.get(1, 0) != itsCount.get(3, 0):
                    self.output("顺的长度和单牌个数对不上")
                    return "不合法"
                return f"三顺{itsCount.get(3, 0)}带单"
            if itsCount.get(2, 0) != 0:
                if itsCount.get(2, 0) != itsCount.get(3, 0):
                    self.output("顺的长度和对子个数对不上")
                    return "不合法"
                return f"三顺{itsCount.get(3, 0)}带双"
            self.output("这种报错，我也不知道怎么搞的")
            return "不合法"
        if itsCount.get(2, 0) >= 3 and itsCount.get(1, 0) == 0 and itsCount.get(4, 0) == 0 and itsCount.get(3,
                                                                                                            0) == 0:
            firstPokerLevel = None
            for i in need:
                if need.get(i) == 2:
                    firstPokerLevel = self.getLevel(i)
                    break
            for i in range(0, itsCount.get(2, 0)):
                if need.get(self.getPoker(firstPokerLevel + i), 0) != 2:
                    self.output("试图出连对但是不那么连续")
                    return "不合法"
            return f"连对{itsCount.get(2, 0)}"
        if itsCount.get(1, 0) >= 5 and itsCount.get(4, 0) == 0 and itsCount.get(2, 0) == 0 and itsCount.get(3,
                                                                                                            0) == 0:
            firstPokerLevel = None
            for i in need:
                if need.get(i) == 1:
                    firstPokerLevel = self.getLevel(i)
                    break
            for i in range(0, itsCount.get(1, 0)):
                if need.get(self.getPoker(firstPokerLevel + i), 0) != 1 or firstPokerLevel + i >= self.getLevel(
                        '鬼'):
                    self.output("试图出顺子，但是不连续")
                    return "不合法"
            return f"顺子{itsCount.get(1, 0)}"
        if itsCount.get(2, 0) == 1 and itsCount.get(1, 0) == 0 and itsCount.get(3, 0) == 0 and itsCount.get(4,
                                                                                                            0) == 0:
            return "对子"
        if itsCount.get(1, 0) == 1 and itsCount.get(2, 0) == 0 and itsCount.get(3, 0) == 0 and itsCount.get(4,
                                                                                                            0) == 0:
            return "单张"
        self.output("这...我对照了一下，这好像匹配不上吧...")
        return "不合法"

    def getPoker(self, index):
        return self.levelPoker.get(index, '空')

    def getLevel(self, poker):
        return self.pokerLevel.get(poker, -1)

    def getIndex(self, number):
        return self.index.get(number, -1)

    def getPokerNumber(self, number, p):
        return self.poker[self.getIndex(number)].get(p, 0)

    def sentPokerMsg(self, qq):
        self.autoBot.send_friend_msg(
            qq,
            f"你的牌:\n{self.queryPoker(qq)}"
        )

    def deletePoker(self, number):
        for i in self.autoPoker:
            self.poker[self.getIndex(number)][i] -= self.autoPoker.get(i)
        res = 0
        for i in self.poker[self.getIndex(number)]:
            res += self.getPokerNumber(number, i)
        return res

    def running(self):
        if self.autoPlain == "加入斗地主" or self.autoPlain == "加入反常斗地主":
            if self.nowState != "等待玩家":
                self.output("等他们这把结束再说吧...")
                return
            for qq in self.numbersQQ:
                if qq == self.autoFriendNumber:
                    self.output("你已经在桌上了，难不成想自己和自己玩？")
                    return

            if self.playModel == "经典模式" and self.autoPlain == "加入反常斗地主":
                self.output("已经有人开了经典模式了，你等他们这把结束再说吧...")
                return
            if self.playModel == "反常模式" and self.autoPlain == "加入斗地主":
                self.output("已经有人开了反常模式了，你等他们这把结束再说吧...")
                return
            if self.autoPlain == "加入斗地主":
                self.playModel = "经典模式"
            else:
                self.playModel = "反常模式"

            self.addPlayer(self.autoFriendNumber)
            if self.nowNumber == 3:
                self.output("加入成功，人数已满，本局开始！")
                #   洗牌发牌
                for qq in self.numbersQQ:
                    self.sentPokerMsg(qq)
                self.nowState = "叫地主"
                self.output("玩家的牌已经私发给玩家", False)
                self.output(f"接下来有请玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】进行操作", False)
                self.output("叫地主环节，可发送[叫地主]或[不叫]来进行操作", False)
            else:
                self.output(f"加入成功，目前已有{self.nowNumber}人")
            return

        if self.autoFriendNumber not in self.numbersQQ:
            return

        if self.autoPlain == "掀桌":
            self.output("有人掀桌，游戏状态已重置", False)
            # addPersonalScore(self.autoFriendNumber, -1)
            self.init()
            # if getPersonalScore(self.autoFriendNumber) > 0:
            # else:
            #     self.output('你的积分不够扣取1分，掀桌失败(强制上桌[doge])')
            return
        if self.nowPlayer != self.getIndex(self.autoFriendNumber):
            return
        if self.autoPlain == "叫地主" and self.nowPlayer == self.getIndex(self.autoFriendNumber) and self.nowState == "叫地主":
            self.output(f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】叫地主")
            self.reserveLandLord.append(self.index[self.autoFriendNumber])
            if self.nowPlayer == 2:
                randIndex = random.randint(0, len(self.reserveLandLord) - 1)
                randIndex = self.reserveLandLord[randIndex]
                self.output(f"玩家【{self.name.get(str(self.numbersQQ[randIndex]), '无名氏')}】成为地主", False)
                for i in range(51, 54):
                    self.poker[randIndex][self.allPokers[i]] = self.poker[randIndex].get(self.allPokers[i], 0) + 1
                self.sentPokerMsg(self.numbersQQ[randIndex])
                # for i in range(0, 3):
                #     self.itsLess[i] = (i == randIndex)
                self.output("接下来请地主先出牌", False)
                self.output("出牌格式示例：[出牌 910JQK]\n本示例出的牌为顺子[9,10,J,Q,K]", False)
                self.landLord = randIndex
                self.nowPlayer = randIndex
                self.lastIndex = randIndex
            else:
                self.nowPlayer += 1
                self.output(f"接下来有请玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】进行操作", False)
                self.output("抢地主环节，可发送[抢地主]或[不抢]来进行操作", False)
                self.nowState = "抢地主"
        if self.autoPlain == "抢地主" and self.nowPlayer == self.getIndex(self.autoFriendNumber) and self.nowState == "抢地主":
            self.output(f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】抢地主", False)
            self.reserveLandLord.append(self.index[self.autoFriendNumber])
            if self.nowPlayer == 2:
                randIndex = random.randint(0, len(self.reserveLandLord) - 1)
                randIndex = self.reserveLandLord[randIndex]
                self.output(f"玩家【{self.name.get(str(self.numbersQQ[randIndex]), '无名氏')}】成为地主", False)
                for i in range(51, 54):
                    self.poker[randIndex][self.allPokers[i]] = self.poker[randIndex].get(self.allPokers[i], 0) + 1
                self.sentPokerMsg(self.numbersQQ[randIndex])
                self.output("接下来请地主先出牌", False)
                # if self.playModel == "反常模式":
                #     for i in range(0, 3):
                #         self.itsLess[i] = (i == randIndex)
                self.output("出牌格式示例：[出牌 910JQK]\n本示例出的牌为顺子[9,10,J,Q,K]", False)
                self.landLord = randIndex
                self.nowPlayer = randIndex
                self.lastIndex = randIndex
            else:
                self.nowPlayer += 1
                self.output(f"接下来有请玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】进行操作", False)
                self.output("抢地主环节，可发送[抢地主]或[不抢]来进行操作", False)
        if self.autoPlain == "不叫" and self.nowPlayer == self.getIndex(self.autoFriendNumber) and self.nowState == "叫地主":
            self.output(f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】不叫")
            if self.nowPlayer == 2:
                if len(self.reserveLandLord) == 0:
                    randIndex = random.randint(0, 2)
                else:
                    randIndex = random.randint(0, len(self.reserveLandLord) - 1)
                    randIndex = self.reserveLandLord[randIndex]
                self.output(f"玩家【{self.name.get(str(self.numbersQQ[randIndex]), '无名氏')}】成为地主", False)

                for i in range(51, 54):
                    self.poker[randIndex][self.allPokers[i]] = self.poker[randIndex].get(self.allPokers[i], 0) + 1
                self.sentPokerMsg(self.numbersQQ[randIndex])
                self.output("接下来请地主先出牌")
                # if self.playModel == "反常模式":
                #     for i in range(0, 3):
                #         self.itsLess[i] = (i == randIndex)
                self.output("出牌格式示例：[出牌 910JQK]\n本示例出的牌为顺子[9,10,J,Q,K]")
                self.landLord = randIndex
                self.nowPlayer = randIndex
                self.lastIndex = randIndex
            else:
                self.nowPlayer += 1
                self.output(f"接下来有请玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】进行操作")
                self.output("叫地主环节，可发送[叫地主]或[不叫]来进行操作")
        if self.autoPlain == "不抢" and self.nowPlayer == self.getIndex(self.autoFriendNumber) and self.nowState == "抢地主":
            self.output(f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】不抢")
            if self.nowPlayer == 2:
                if len(self.reserveLandLord) == 0:
                    randIndex = random.randint(0, 2)
                else:
                    randIndex = random.randint(0, len(self.reserveLandLord) - 1)
                    randIndex = self.reserveLandLord[randIndex]
                self.output(f"玩家【{self.name.get(str(self.numbersQQ[randIndex]), '无名氏')}】成为地主")
                for i in range(51, 54):
                    self.poker[randIndex][self.allPokers[i]] = self.poker[randIndex].get(self.allPokers[i], 0) + 1
                self.sentPokerMsg(self.numbersQQ[randIndex])
                self.output("接下来请地主先出牌")
                if self.playModel == "反常模式":
                    for i in range(0, 3):
                        self.itsLess[i] = (i == randIndex)
                self.output("出牌格式示例：[出牌 910JQK]\n本示例出的牌为顺子[9,10,J,Q,K]\n过牌请发送[过]")
                self.landLord = randIndex
                self.nowPlayer = randIndex
                self.lastIndex = randIndex
            else:
                self.nowPlayer += 1
                self.output(f"接下来有请玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】进行操作")
                self.output("抢地主环节，可发送[抢地主]或[不抢]来进行操作")
        if re.match("出牌 .*", self.autoPlain):
            self.autoModel = self.checkPoker(self.autoFriendNumber, self.autoArguments[1])
            if self.compare(self.itsLess[self.nowPlayer]) or (
                    self.lastIndex == self.getIndex(self.autoFriendNumber) and self.autoModel != "不合法"):
                if self.deletePoker(self.autoFriendNumber) == 0:
                    self.output(
                        f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】出牌:\n{self.autoArguments[1]}\n牌型【{self.autoModel}】")
                    if self.landLord == self.getIndex(self.autoFriendNumber):
                        self.output(
                            f"地主玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】获得胜利！积分+2!\n两平民积分各自-1!")
                        for i in range(0, 3):
                            qq = self.numbersQQ[i]
                            if i == self.landLord:
                                self.addPersonalScore(qq, 2)
                            else:
                                self.addPersonalScore(qq, -1)
                    else:
                        self.output(
                            f"平民玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】获得胜利！平民玩家各自积分+1!\n地主积分-2!")
                        for i in range(0, 3):
                            qq = self.numbersQQ[i]
                            if i == self.landLord:
                                self.addPersonalScore(qq, -2)
                            else:
                                self.addPersonalScore(qq, 1)
                    self.output("本局对局结束！切换为等待状态...可发送[加入斗地主]进行加入...")
                    self.init()
                else:
                    self.output(
                        f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】出牌:\n{self.autoArguments[1]}\n牌型【{self.autoModel}】")
                    if self.playModel == "反常模式":
                        self.itsLess[self.nowPlayer] ^= True
                    self.lastIndex = self.nowPlayer
                    self.sentPokerMsg(self.autoFriendNumber)
                    self.nowPlayer += 1
                    self.nowPlayer %= 3
                    self.lastModel = self.autoModel
                    self.lastPoker = self.autoPoker
                    self.output(
                        f"接下来有请玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】进行操作\n玩家逆序状态：【{self.itsLess[self.nowPlayer]}】")
            else:
                self.output(f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】,不如你再仔细看看？你出的啥啊.")
                self.output("你重新出牌吧")
                self.output(f"对了，你刚才的牌型是【{self.autoModel}】\n要么你牌型对不上，要么你出的没比别人的大或者小")
        if self.autoPlain == "过" and self.lastModel != "空":
            self.output(
                f"玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】过牌")
            if self.playModel == "反常模式":
                self.itsLess[self.nowPlayer] ^= True
            self.sentPokerMsg(self.autoFriendNumber)
            self.nowPlayer += 1
            self.nowPlayer %= 3
            self.output(
                f"接下来有请玩家【{self.name.get(str(self.numbersQQ[self.nowPlayer]), '无名氏')}】进行操作\n玩家逆序状态：【{self.itsLess[self.nowPlayer]}】")

    def getState(self):
        return self.nowState
