# -*- coding: utf-8 -*-
import random
import threading
import miraicle
import json
import re
import time
import requests
import MoveStoneGame
import MoveStoneGameBotModel
import FightTheLandlordGame
import miraicle.createImg as createImg
from requests.packages import urllib3

urllib3.disable_warnings()
groupList = []
finishSign = False
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
lastSender = {}
lianCount = {}
msgCount = {}
countLimitPath = ".\\Data\\countLimit.txt"
countLimit = {}
bannedWordsPath = ".\\Data\\bannedWords.txt"
bannedWords = {}
bannedWordsMuteStatePath = ".\\Data\\bannedWordsMuteState.txt"
bannedWordsMuteState = {}
bannedWordsMuteTimePath = ".\\Data\\bannedWordsMuteTime.txt"
bannedWordsMuteTime = {}
passOnAMsgStatePath = ".\\Data\\passOnAMsgState.txt"
passOnAMsgState = {}
refusePassOnAMsgStatePath = ".\\Data\\refusePassOnAMsgState.txt"
refusePassOnAMsgState = {}
codeforcesNamePath = ".\\Data\\codeforcesName.txt"
codeforcesName = {}
contestInformListPath = ".\\Data\\contestInformList.txt"
contestInformList = {}
groupMoveStone = {}
personalMoveStone = {}
groupFightTheLandlord = {}
groupKickBotNumberPath = ".\\Data\\groupKickBotNumber.txt"
groupKickBotNumber = {}
lastRecallMsg = {}


with open(userScorePath, 'r') as f:
    userScore = json.load(f)
with open(msgMatchPath, 'r') as f:
    msgMatch = json.load(f)
with open(adminPath, 'r') as f:
    admin = json.load(f)
with open(namePath, 'r') as f:
    name = json.load(f)
with open(teaRoomStatePath, 'r') as f:
    teaRoomState = json.load(f)
with open(teaRoomAutoStatePath, 'r') as f:
    teaRoomAutoState = json.load(f)
with open(countLimitPath, 'r') as f:
    countLimit = json.load(f)
with open(bannedWordsPath, 'r') as f:
    bannedWords = json.load(f)
with open(passOnAMsgStatePath, 'r') as f:
    passOnAMsgState = json.load(f)
with open(codeforcesNamePath, 'r') as f:
    codeforcesName = json.load(f)
with open(contestInformListPath, 'r') as f:
    contestInformList = json.load(f)
with open(bannedWordsMuteTimePath, 'r') as f:
    bannedWordsMuteTime = json.load(f)
with open(bannedWordsMuteStatePath, 'r') as f:
    bannedWordsMuteState = json.load(f)
with open(refusePassOnAMsgStatePath, 'r') as f:
    refusePassOnAMsgState = json.load(f)
with open(groupKickBotNumberPath, 'r') as f:
    groupKickBotNumber = json.load(f)


def getCodeForcesContestInfo():
    temp = requests.get("https://codeforces.com/api/contest.list?gym=false", verify=False)
    if temp.status_code == 404:
        return "接口暂时无响应，请等待几分钟后再试哦~"
    response = temp.json()
    if response.get('status', 'FAILED') == 'FAILED':
        return "获取信息失败..."
    else:
        Str = "CF近期比赛列表(5天内):"
        Max = 30
        List = response.get('result', [])
        for dic in List:
            temp = time.time()
            startTime = dic.get('startTimeSeconds', 0)
            if temp > startTime or temp + 432000 < startTime:
                continue
            Str += '\n'
            Str += "---------------------------------\n"
            Str += f"比赛ID: {dic.get('id', 0)}\n"
            Str += f"比赛名称: {dic.get('name', '[未知错误]')}\n"
            Str += f"比赛来源: {dic.get('type', '[未知错误]')}\n"
            ti = time.gmtime(startTime)
            Str += f"比赛时间:{'%04d' % ti.tm_year}-{'%02d' % ti.tm_mon}-{'%02d' % (ti.tm_mday + int((ti.tm_hour+8)/24))} {'%02d' % int((ti.tm_hour + 8)%24)}:{'%02d' % ti.tm_min}:{'%02d' % ti.tm_sec}\n"
            temp = dic.get('durationSeconds', 0)
            Str += f"比赛时长: {'%02d'%int(temp/3600)}:{'%02d'%int((temp%3600)/60)}:{'%02d'%int(temp%60)}\n"
            Max -= 1
            if not Max:
                break
        if Str == "CF近期比赛列表(5天内):":
            Str += "\n近期暂无比赛..."
        return Str


class _Info:
    autoBot = None
    autoGroupNumber = None
    autoFriendNumber = None
    autoPlain = None
    autoMsgJson = None
    autoFullMsg = None
    autoNoSpaceMsg = None
    autoName = None
    autoMsgId = None
    autoArguments = []
    autoImage = None
    isFriend = False
    autoAtQQ = []


@miraicle.scheduled_job(miraicle.Scheduler.every(60).seconds)
def update(bot):
    updateGroupList(bot.group_list().get('data', []))
    with open(userScorePath, 'w') as f:
        f.write(json.dumps(userScore))
    with open(msgMatchPath, 'w') as f:
        f.write(json.dumps(msgMatch))
    with open(adminPath, 'w') as f:
        f.write(json.dumps(admin))
    with open(namePath, 'w') as f:
        f.write(json.dumps(name))
    with open(teaRoomStatePath, 'w') as f:
        f.write(json.dumps(teaRoomState))
    with open(teaRoomAutoStatePath, 'w') as f:
        f.write(json.dumps(teaRoomAutoState))
    with open(countLimitPath, 'w') as f:
        f.write(json.dumps(countLimit))
    with open(bannedWordsPath, 'w') as f:
        f.write(json.dumps(bannedWords))
    with open(passOnAMsgStatePath, 'w') as f:
        f.write(json.dumps(passOnAMsgState))
    with open(codeforcesNamePath, 'w') as f:
        f.write(json.dumps(codeforcesName))
    with open(contestInformListPath, 'w') as f:
        f.write(json.dumps(contestInformList))
    with open(bannedWordsMuteTimePath, 'w') as f:
        f.write(json.dumps(bannedWordsMuteTime))
    with open(bannedWordsMuteStatePath, 'w') as f:
        f.write(json.dumps(bannedWordsMuteState))
    with open(refusePassOnAMsgStatePath, 'w') as f:
        f.write(json.dumps(refusePassOnAMsgState))
    with open(groupKickBotNumberPath, 'w') as f:
        f.write(json.dumps(groupKickBotNumber))


@miraicle.scheduled_job(miraicle.Scheduler.every().day.at('12:00:00'))
def sendContestInfo(bot:miraicle.Mirai):
    temp = requests.get("https://codeforces.com/api/contest.list?gym=false", verify=False)
    if temp.status_code == 404:
        print("Log : 接口暂时无响应")
    response = temp.json()
    if response.get('status', 'FAILED') == 'FAILED':
        return
    else:
        Str = "今天有比赛要举行哦~:"
        Max = 30
        List = response.get('result', [])
        for dic in List:
            temp = time.time()
            startTime = dic.get('startTimeSeconds', 0)
            if temp > startTime or temp + 43200 < startTime:
                continue
            Str += '\n'
            Str += "---------------------------------\n"
            Str += f"比赛ID: {dic.get('id', 0)}\n"
            Str += f"比赛名称: {dic.get('name', '[未知错误]')}\n"
            Str += f"比赛来源: {dic.get('type', '[未知错误]')}\n"
            ti = time.gmtime(startTime)
            Str += f"比赛时间:{'%04d' % ti.tm_year}-{'%02d' % ti.tm_mon}-{'%02d' % (ti.tm_mday + int((ti.tm_hour + 8) / 24))} {'%02d' % int((ti.tm_hour + 8) % 24)}:{'%02d' % ti.tm_min}:{'%02d' % ti.tm_sec}\n"
            temp = dic.get('durationSeconds', 0)
            Str += f"比赛时长: {'%02d' % int(temp / 3600)}:{'%02d' % int((temp % 3600) / 60)}:{'%02d' % int(temp % 60)}\n"
            Max -= 1
            if not Max:
                break
        if Str == "今天有比赛要举行哦~:":
            return
        info = _Info()
        info.autoBot = bot
        info.isFriend = True
        for qq in contestInformList:
            if not contestInformList.get(str(qq), False):
                continue
            info.autoFriendNumber = int(qq)
            output(info, Str)


@miraicle.scheduled_job(miraicle.Scheduler.every().day.at('00:00:00'))
def clearTeaRoomState(bot: miraicle.Mirai):
    updateTime()
    info = _Info()
    info.autoBot = bot
    info.autoFriendNumber = 1784518480
    info.autoName = getName(info.autoFriendNumber)
    sentTeaRoomMessage(info, "[茶馆已闭馆]这位客官，此刻入夜已深，尽早歇息去罢。\n若仍要在茶馆落脚，可再次发送[进入茶馆]。")
    for qq in teaRoomState:
        if qq == 'online':
            teaRoomState[qq] = 0
        else:
            teaRoomState[qq] = False


@miraicle.Mirai.receiver('BotLeaveEventKick')
def solveKickBotMessage(bot: miraicle.Mirai, msg: json):
    groupId = msg.get('group', {}).get('id', 0)
    groupKickBotNumber[str(groupId)] = getKickBotNumber(groupId) + 1


def getKickBotNumber(groupId):
    return groupKickBotNumber.get(str(groupId), 0)


@miraicle.Mirai.receiver('BotInvitedJoinGroupRequestEvent')
def solveInvitedMessage(bot: miraicle.Mirai, msg: json):
    if not admin.get("kickBotRefuse", False):
        bot.handle_group_invation(msg.get('eventId', 0), msg.get('fromId', 0), msg.get('groupId', 0), 0)
        return
    if getKickBotNumber(msg.get('groupId', 0)) > 0:
        bot.handle_group_invation(msg.get('eventId', 0), msg.get('fromId', 0), msg.get('groupId', 0), 1)
    else:
        bot.handle_group_invation(msg.get('eventId', 0), msg.get('fromId', 0), msg.get('groupId', 0), 0)


@miraicle.Mirai.receiver('MemberMuteEvent')
def solveGroupMuteEvent(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    qq = msg.get('member', {}).get('id', 0)
    group = msg.get('member', {}).get('group', {}).get('id', 0)
    if isAdmin(qq):
        bot.unmute(group, qq)


@miraicle.Mirai.receiver('GroupMessage')
def solveGroupMessage(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    # if msg.group != 261925581:
    #     return
    updateTime()
    info = _Info()
    info.autoArguments = msg.plain.split()
    info.isFriend = False
    info.autoBot = bot
    info.autoGroupNumber = msg.group
    info.autoPlain = msg.plain
    info.autoMsgJson = msg.json
    info.autoImage = msg.first_image
    info.autoFriendNumber = msg.sender
    info.autoName = msg.sender_name
    info.autoMsgId = msg.id
    info.autoAtQQ = getAllAtQQ(info.autoMsgJson)
    info.autoNoSpaceMsg = getNoSpaceMsg(info.autoPlain)
    info.autoFullMsg = getFullMsgInfo(info.autoMsgJson)
    if getName(info.autoFriendNumber) == "无名氏":
        setName(info, info.autoName)
    # changeLastSendGroup(info.autoFriendNumber, info.autoGroupNumber)
    temp = time.time()
    addMsgCount(info.autoGroupNumber, info.autoFriendNumber, temp)
    global lianCount
    if lastSender.get(info.autoGroupNumber, 0) == info.autoFriendNumber:
        lianCount[info.autoFriendNumber] = lianCount.get(info.autoFriendNumber, 0) + 1
    else:
        lianCount[info.autoFriendNumber] = 0
        lastSender[info.autoGroupNumber] = info.autoFriendNumber

    signNum = 0
    for c in info.autoPlain:
        if c == "\n":
            signNum += 1
    for i in range(0, int(signNum/3)):
        addMsgCount(info.autoGroupNumber, info.autoFriendNumber, temp)
    if getMsgCount(info.autoGroupNumber, info.autoFriendNumber) > getCountLimit(info.autoGroupNumber) or\
            lianCount.get(info.autoFriendNumber, 0) > getCountLimit(info.autoGroupNumber):
        info.autoBot.mute(info.autoGroupNumber, info.autoFriendNumber, 600)
        addMsgCount(info.autoGroupNumber, info.autoFriendNumber, 0)
        output(info, "请不要刷屏", True)
        lianCount[info.autoFriendNumber] = 0
    t1 = threading.Thread(target=runningMoveStoneGame, args=(info,))
    t2 = threading.Thread(target=runningFightTheLandlordGame, args=(info,))
    t3 = threading.Thread(target=messageMatchReply, args=(info,))
    t1.start()
    t2.start()
    t3.start()
    # runningMoveStoneGame(info)
    # runningFightTheLandlordGame(info)
    # messageMatchReply(info)


@miraicle.Mirai.receiver('TempMessage')
def solveTempMessage(bot: miraicle.Mirai, msg: miraicle.TempMessage):
    updateTime()
    info = _Info()
    info.autoArguments = msg.plain.split()
    info.isFriend = True
    info.autoBot = bot
    info.autoPlain = msg.plain
    info.autoMsgJson = msg.json
    info.autoImage = msg.first_image
    info.autoFriendNumber = msg.sender
    info.autoName = msg.sender_name
    info.autoFullMsg = getFullMsgInfo(info.autoMsgJson)
    info.autoNoSpaceMsg = getNoSpaceMsg(info.autoPlain)
    if getName(info.autoFriendNumber) == "无名氏":
        setName(info, info.autoName)
    messageMatchReply(info)


@miraicle.Mirai.receiver('StrangerMessage')
def solveStrangerMessage(bot: miraicle.Mirai, msg: miraicle.TempMessage):
    updateTime()
    info = _Info()
    info.autoPlain = ''
    for dic in msg.get('messageChain', []):
        if dic.get('type', None) == 'Plain':
            info.autoPlain += dic.get('text', '')
    info.autoArguments = info.autoPlain.split()
    info.isFriend = True
    info.autoBot = bot
    info.autoMsgJson = msg
    info.autoFriendNumber = msg.get('sender', {}).get('id', 0)
    info.autoName = msg.get('sender', {}).get('nickname', '-')
    info.autoFullMsg = getFullMsgInfo(info.autoMsgJson)
    info.autoNoSpaceMsg = getNoSpaceMsg(info.autoPlain)
    if getName(info.autoFriendNumber) == "无名氏":
        setName(info, info.autoName)
    messageMatchReply(info)


@miraicle.Mirai.receiver('FriendMessage')
def solveFriendMessage(bot: miraicle.Mirai, msg: miraicle.FriendMessage):
    updateTime()
    info = _Info()
    info.autoArguments = msg.plain.split()
    info.isFriend = True
    info.autoBot = bot
    info.autoPlain = msg.plain
    info.autoMsgJson = msg.json
    info.autoImage = msg.first_image
    info.autoFriendNumber = msg.sender
    info.autoName = msg.sender_name
    info.autoFullMsg = getFullMsgInfo(info.autoMsgJson)
    info.autoNoSpaceMsg = getNoSpaceMsg(info.autoPlain)
    if info.autoFriendNumber == 1924645279:
        if msg.plain == "被踢自动拒绝邀请":
            admin["kickBotRefuse"] = True
            output(info, "已更新")
        if msg.plain == "被踢不自动拒绝邀请":
            admin["kickBotRefuse"] = False
            output(info, "已更新")
        if msg.plain == "清空被踢数据":
            clearKickBotNumber()
            output(info, "已清空")
        someTest(info)
    if getName(info.autoFriendNumber) == "无名氏":
        setName(info, info.autoName)
    if re.match("更新数据", info.autoPlain) and info.autoFriendNumber == 1924645279:
        update(bot)
        output(info, '完成！')
        return
    messageMatchReply(info)


def someTest(info):
    pass


def clearKickBotNumber():
    for group in groupKickBotNumber:
        groupKickBotNumber[group] = 0


def changeContestInfoStatue(qq, statue):
    contestInformList[str(qq)] = statue


def getCodeforcesName(qq):
    return codeforcesName.get(str(qq), None)


def setCodeforcesName(qq, Str):
    codeforcesName[str(qq)] = Str


def getCodeforcesUserInfo(info):
    if getCodeforcesName(info.autoFriendNumber) is None:
        output(info, "你尚未设置自己的CF昵称，因此无法查询信息。")
        return
    temp = requests.get(f"https://codeforces.com/api/user.info?handles={getCodeforcesName(info.autoFriendNumber)}", verify=False)
    if temp.status_code == 404:
        output(info, "接口暂时无响应，请等待几分钟后再试哦~")
    response = temp.json()
    if response.get('status', 'FAILED') == 'FAILED':
        output(info, "获取信息失败...")
        return
    else:
        List = response.get('result', [])
        Str = ""
        for dic in List:
            img = miraicle.Image(url=dic.get('titlePhoto', None))
            Str += f"\n个人昵称:{dic.get('handle', '[未知错误]')}"
            Str += f"\nFriendOfCount:{dic.get('friendOfCount', '[未知错误]')}"
            Str += f"\nContribution:{dic.get('contribution', '[未知错误]')}"
            Str += f"\nRating:{dic.get('rating', '[未知错误]')}"
            Str += f"\nMaxRating:{dic.get('maxRating', '[未知错误]')}"
            Str += f"\nMaxRank:{dic.get('maxRank', '[未知错误]')}"
            output(info, Str, topImg=img)
            return


def updateGroupList(List):
    global groupList
    groupList.clear()
    for dic in List:
        groupList.append(dic.get('id', 0))


def queryPassOnAMsgNumber(number):
    return passOnAMsgState.get(str(number), 0)


def setPassOnAMsgNumber(number, qq):
    passOnAMsgState[str(number)] = int(qq)


def getPassOnAMsgNumber(number):
    return int(passOnAMsgState.get(str(number), 0))


def getBannedWordsList(groupNumber):
    Str = ""
    for word in bannedWords.get(str(groupNumber), {}):
        if bannedWords.get(str(groupNumber), {}).get(word, False):
            Str += f" {word} "
    if Str == "":
        return "[没有违禁词...]"
    return Str


def checkExistBannedWords(groupNumber, Str):
    for word in bannedWords.get(str(groupNumber), {}):
        if bannedWords.get(str(groupNumber), {}).get(word, False) and Str.find(word) != -1:
            return True
    return False


def setBannedWordsMuteState(groupNumber, ifMute):
    bannedWordsMuteState[str(groupNumber)] = ifMute


def getBannedWordsMuteState(groupNumber):
    return bannedWordsMuteState.get(str(groupNumber), False)


def setBannedWordsMuteTime(groupNumber, Time):
    bannedWordsMuteTime[str(groupNumber)] = int(Time)


def getBannedWordsMuteTime(groupNumber):
    return bannedWordsMuteTime.get(str(groupNumber), 3)


def addBannedWords(groupNumber, List):
    if bannedWords.get(str(groupNumber), {}) == {}:
        bannedWords[str(groupNumber)] = {}
    for word in List:
        bannedWords[str(groupNumber)][str(word)] = True


def deleteAllBannedWords(groupNumber):
    bannedWords[str(groupNumber)] = {}


def deleteBannedWords(groupNumber, List):
    if bannedWords.get(str(groupNumber), {}) == {}:
        bannedWords[str(groupNumber)] = {}
    for word in List:
        bannedWords[str(groupNumber)][str(word)] = False


def getNoSpaceMsg(Str):
    List = Str.split()
    ans = ""
    for cnt in List:
        ans += cnt
    return ans


def getCountLimit(groupNumber):
    return countLimit.get(str(groupNumber), 10)


def setCountLimit(groupNumber, val):
    countLimit[str(groupNumber)] = int(val)


def addMsgCount(groupNumber, number, Time):
    if not msgCount.get(str(groupNumber), {}):
        msgCount[str(groupNumber)] = {}
    if not msgCount[str(groupNumber)].get(str(number), []):
        msgCount[str(groupNumber)][str(number)] = []
    tempLis = []
    for t in msgCount[str(groupNumber)][str(number)]:
        if t < Time - 10 or t > Time:
            continue
        tempLis.append(t)
    msgCount[str(groupNumber)][str(number)] = tempLis
    msgCount[str(groupNumber)][str(number)].append(Time)


def getMsgCount(groupNumber, number):
    if not msgCount.get(str(groupNumber), {}):
        msgCount[str(groupNumber)] = {}
    if not msgCount[str(groupNumber)].get(str(number), []):
        msgCount[str(groupNumber)][str(number)] = []
    return len(msgCount[str(groupNumber)][str(number)])


def messageMatchReply(info):
    t1 = threading.Thread(target=runningMoveStoneGameBotModel, args=(info,))
    t1.start()
    # runningMoveStoneGameBotModel(info)
    if re.match("开启cf比赛提醒", info.autoPlain):
        output(info, "好的")
        changeContestInfoStatue(info.autoFriendNumber, True)
        return
    if re.match("关闭cf比赛提醒", info.autoPlain):
        output(info, "好的")
        changeContestInfoStatue(info.autoFriendNumber, False)
        return
    if re.match("cf昵称 .*", info.autoPlain):
        setCodeforcesName(info.autoFriendNumber, info.autoArguments[1])
        output(info, "更新完毕")
        return
    if re.match("查询cf比赛", info.autoPlain):
        output(info, "正在查询中...请耐心等待...")
        output(info, getCodeForcesContestInfo())
        return
    if re.match("查询个人cf", info.autoPlain):
        output(info, "正在查询中...请耐心等待...")
        getCodeforcesUserInfo(info)
        return
    if re.match("拒绝被传话", info.autoPlain):
        output(info, "好的")
        setRefusePassOnAMsgState(info.autoFriendNumber, True)
        return
    if re.match("允许被传话", info.autoPlain):
        output(info, "好的")
        setRefusePassOnAMsgState(info.autoFriendNumber, False)
        return
    if re.match("违禁词列表", info.autoPlain):
        showBannedWordsList(info)
        return
    if info.autoPlain == "开启便捷茶馆":
        output(info, "好的", True)
        setTeaRoomAutoState(info.autoFriendNumber, True)
        return
    if info.autoPlain == "关闭便捷茶馆":
        output(info, "好的", True)
        setTeaRoomAutoState(info.autoFriendNumber, False)
        return
    if re.match("添加管理员", info.autoNoSpaceMsg) is not None and len(info.autoAtQQ) > 0:
        if info.autoFriendNumber != owner:
            output(info,  "你不是墨晓晓！", True)
        else:
            output(info,  "好的", True)
            for qq in info.autoAtQQ:
                addAdministrator(qq)
        return
    if re.match("删除管理员", info.autoNoSpaceMsg) is not None and len(info.autoAtQQ) > 0:
        if info.autoFriendNumber != owner:
            output(info, "你不是墨晓晓！", True)
        else:
            output(info, "好的", True)
            for qq in info.autoAtQQ:
                deleteAdministrator(qq)
        return
    if re.match("设置昵称 .*", info.autoPlain) is not None:
        if len(info.autoArguments[1]) <= 20:
            output(info, "好的", True)
            setName(info, info.autoArguments[1])
        else:
            output(info, "不行，你昵称太长了", True)
        return
    if re.match("茶馆 .*", info.autoPlain) is not None:
        updateTime()
        if getTeaState(info.autoFriendNumber):
            if not info.isFriend:
                output(info, f"[online:{getTeaRoomPeopleNumber()}]好嘞，小的这就帮您转达", True)
            Str = ""
            for i in info.autoArguments[1:]:
                Str += i
                Str += ' '
            if info.autoImage is not None:
                Str += f"[mirai:image:{info.autoImage.image_id}]"
            sentTeaRoomMessage(info, Str)
        else:
            output(info, "您这不还没进茶馆嘛...", True)
        return
    if re.match("反馈 .*", info.autoPlain) is not None:
        Str = ""
        for i in info.autoArguments[1:]:
            Str += i
            Str += ' '
        output(info, "您的反馈已发送到开发组，感谢您的宝贵建议", True)
        sentFeedBackMessage(info, f"收到一条反馈信息:\n{Str}")
        return
    if info.autoPlain == "茶馆在线列表":
        output(info, queryTeaRoomOnlineList())
        return
    if info.autoPlain == "菜单":
        showMenu(info)
        return
    if info.autoPlain == "进入茶馆":
        if getTeaState(info.autoFriendNumber):
            output(info, "客官您已经在茶馆里了", True)
        else:
            output(info, "好的", True)
            setTeaRoomState(info.autoFriendNumber, True)
            output(info, f"当前在线人数:{getTeaRoomPeopleNumber()}")
        return
    if info.autoPlain == "离开茶馆":
        if getTeaState(info.autoFriendNumber):
            output(info, "好的", True)
            setTeaRoomState(info.autoFriendNumber, False)
        else:
            output(info, "客官您本就不在茶馆之中", True)
        return
    if not info.isFriend:
        haveAdm = (info.autoBot.is_owner(info.autoFriendNumber, info.autoGroupNumber) or
                   info.autoBot.is_administrator(info.autoFriendNumber, info.autoGroupNumber))

        if re.match("添加违禁词 .*", info.autoPlain) and (isAdmin(info.autoFriendNumber) or haveAdm):
            output(info, "好的")
            addBannedWords(info.autoGroupNumber, info.autoArguments[1:])
            return
        if re.match("删除违禁词 .*", info.autoPlain) and (isAdmin(info.autoFriendNumber) or haveAdm):
            output(info, "好的")
            deleteBannedWords(info.autoGroupNumber, info.autoArguments[1:])
            return
        if re.match("清空违禁词", info.autoPlain) and (isAdmin(info.autoFriendNumber) or haveAdm):
            output(info, "好的")
            deleteAllBannedWords(info.autoGroupNumber)
            return
        if re.match("开启违禁词禁言", info.autoPlain) and (isAdmin(info.autoFriendNumber) or haveAdm):
            output(info, "好的")
            setBannedWordsMuteState(info.autoGroupNumber, True)
            return
        if re.match("关闭违禁词禁言", info.autoPlain) and (isAdmin(info.autoFriendNumber) or haveAdm):
            output(info, "好的")
            setBannedWordsMuteState(info.autoGroupNumber, False)
            return
        if re.match("违禁词禁言时长 [0-9]+", info.autoPlain) and (isAdmin(info.autoFriendNumber) or haveAdm):
            output(info, "好的")
            setBannedWordsMuteTime(info.autoGroupNumber, info.autoArguments[1])
            return
        if re.match("刷屏限制 [0-9]+", info.autoPlain) is not None and (isAdmin(info.autoFriendNumber) or haveAdm):
            output(info, "更改成功")
            setCountLimit(info.autoGroupNumber, info.autoArguments[1])
            return

        if re.match("禁言.*[0-9]+", info.autoPlain):
            if not isAdmin(info.autoFriendNumber) and not haveAdm:
                output(info, "你掺和啥呢..")
            else:
                Failed = 0
                output(info, "行，我试试")
                for qq in info.autoAtQQ:
                    if isAdmin(qq):
                        Failed += 1
                        continue
                    info.autoBot.mute(info.autoGroupNumber, int(qq), min(43200, int(info.autoArguments[1])) * 60)
                if Failed > 0:
                    output(info, f"里面有{Failed}个人是我的管理员，我是不会禁言的")
            return
        if re.match("解除禁言", info.autoNoSpaceMsg) is not None and len(info.autoAtQQ) > 0:
            if not isAdmin(info.autoFriendNumber) and not haveAdm:
                output(info, "你掺和啥呢..")
            else:
                output(info, "行，我试试")
                for qq in info.autoAtQQ:
                    info.autoBot.unmute(info.autoGroupNumber, qq)
            return
        if re.match("踢出", info.autoNoSpaceMsg) is not None and len(info.autoAtQQ) > 0:
            if not isAdmin(info.autoFriendNumber) and not haveAdm:
                output(info, "你掺和啥呢..")
            else:
                Failed = 0
                output(info, "行，我试试")
                for qq in info.autoAtQQ:
                    if isAdmin(qq):
                        Failed += 1
                        continue
                    info.autoBot.kick(info.autoGroupNumber, qq)
                if Failed > 0:
                    output(info, f"里面有{Failed}个人是我的管理员，我是不会踢的")
            return
        if info.autoPlain == "全体禁言":
            if not isAdmin(info.autoFriendNumber) and not haveAdm:
                output(info, "你掺和啥呢..")
            else:
                if not (info.autoBot.is_owner(robotQQ, info.autoGroupNumber) or info.autoBot.is_administrator(robotQQ,
                                                                                               info.autoGroupNumber)):
                    output(info, "啊这,我...我做不到啊")
                else:
                    info.autoBot.mute_all(info.autoGroupNumber)
                    output(info, "好的")
            return
        if info.autoPlain == "解除全体禁言":
            if not isAdmin(info.autoFriendNumber):
                output(info, "你掺和啥呢..")
            else:
                if not (info.autoBot.is_owner(robotQQ, info.autoGroupNumber) or info.autoBot.is_administrator(robotQQ,
                                                                                               info.autoGroupNumber)):
                    output(info, "啊这,我...我做不到啊")
                else:
                    info.autoBot.unmute_all(info.autoGroupNumber)
                    output(info, "好的")
            return
    if info.autoPlain == "我信息呢":
        output(info, "好啦好啦，发给你就是了...")
        output(info, lastRecallMsg.get(f'{str(info.autoFriendNumber)}', ""), personal=True)
        return
    if info.autoPlain == "个人信息":
        queryPersonalInformation(info)
        return
    if info.autoPlain == "设置昵称":
        showSetPersonalNick(info)
        return
    if info.autoPlain == "茶馆系统":
        showTeaRoomSystem(info)
        return
    if info.autoPlain == "群管系统":
        showGroupRegulateSystem(info)
        return
    if info.autoPlain == "反馈系统":
        showFeedBackSystem(info)
        return
    if info.autoPlain == "传话系统":
        showPassOnAMsg(info)
        return
    if info.autoPlain == "便民工具":
        showServiceForCustomers(info)
        return
    if info.autoPlain == "娱乐系统":
        showGameList(info)
        return
    if info.autoPlain == "积分排行":
        showScoreRank(info)
        return
    if info.autoPlain == "挪石头":
        showMoveStoneGame(info)
        return
    if info.autoPlain == "斗地主":
        showFightLandlordGame(info)
        return
    if info.autoPlain == "积分负排行":
        output(info, getScoreRankGreater())
        return
    if info.autoPlain == "积分正排行":
        output(info, getScoreRankLower())
        return
    if info.isFriend:
        if re.match("开始传话 [0-9]+", info.autoPlain):
            if getRefusePassOnAMsgState(info.autoArguments[1]):
                output(info, "对方拒绝被传话")
                return
            output(info, "好的")
            setPassOnAMsgNumber(info.autoFriendNumber, info.autoArguments[1])
            return
        if re.match("结束传话", info.autoPlain):
            output(info, "好的")
            setPassOnAMsgNumber(info.autoFriendNumber, 0)
            return
        if queryPassOnAMsgNumber(info.autoFriendNumber) != 0:
            if getRefusePassOnAMsgState(queryPassOnAMsgNumber(info.autoFriendNumber)):
                output(info, "对方拒绝被传话")
                setPassOnAMsgNumber(info.autoFriendNumber, 0)
                return
            if sentMsgToSomeOne(info, getPassOnAMsgNumber(info.autoFriendNumber), info.autoFullMsg):
                output(info, "传话成功")
            else:
                output(info, "我已经尽力了...但还是没能联系上对方...")
            return
        if getTeaRoomAutoState(info.autoFriendNumber):
            updateTime()
            if getTeaState(info.autoFriendNumber):
                sentTeaRoomMessage(info, getFullMsgInfo(info.autoMsgJson))
            return
    if checkExistBannedWords(info.autoGroupNumber, info.autoNoSpaceMsg) and not info.isFriend:
        output(info, "检测到违禁词")
        lastRecallMsg[str(info.autoFriendNumber)] = info.autoFullMsg
        bot.recall(info.autoMsgId)
        if getBannedWordsMuteState(info.autoGroupNumber):
            info.autoBot.mute(info.autoGroupNumber, int(info.autoFriendNumber), min(43200, int(getBannedWordsMuteTime(info.autoGroupNumber)) * 60))


def showBannedWordsList(info):
    output(info, "请稍等...")
    Str = "违禁词列表：\n"
    len = 0
    lenMax = 200
    textSize = 20
    tempJson = bannedWords.get(str(info.autoGroupNumber), {})
    for words in tempJson:
        if tempJson[words]:
            Str += " "
            for c in words:
                Str += c
                len += textSize
                if len > lenMax*2 - 30:
                    Str += "\n"
                    len = 0
    imgPath = createImg.CreateImg(Str, fontSize=textSize)
    # output(info, f"当前路径为{imgPath}")
    # output(info, rf"{imgPath}")
    img = miraicle.Image(url=rf'{imgPath}')
    output(info,"",topImg=img)


def getScoreRankGreater():
    Str = "积分负排行榜:"
    lis = sorted(userScore.items(), key=lambda x:x[1])
    i = 0
    for it in lis:
        if it[1]>=0:
            break
        Str += f"\n【{getName(it[0])}】({it[0]}): {it[1]}"
        i += 1
        if i == 15:
            break
    return Str


def getScoreRankLower():
    Str = "积分正排行榜:"
    lis = sorted(userScore.items(), key=lambda x:x[1], reverse=True)
    i = 0
    for it in lis:
        if it[1]<=0:
            break
        Str += f"\n【{getName(it[0])}】({it[0]}): {it[1]}"
        i += 1
        if i == 15:
            break
    return Str


def showScoreRank(info):
    Str = "用于获取积分排行，至多只显示前15名\n\
指令如下:\n\
[积分正排行]\n\
[积分负排行]"
    output(info, Str)


def showFightLandlordGame(info):
    Str = "斗地主，经典玩法，需要三名玩家共同游戏，玩家需要添加机器人为好友，以便接收自己的牌信息。其需要用到的指令如下:\n\
[加入斗地主]\n\
[离开斗地主]\n\
[斗地主掀桌](玩家长时间未操作，任意群成员可掀桌)\n\
[斗地主对局信息]\n\
[我牌呢](当你找不到自己的牌时可以发送看看)\n\
[叫地主]\n\
[不叫]\n\
[明牌](仅在开始出牌前可以进行操作)\n\
[出 ***](出自己的牌，字母统一大写)\n\
[过](要不起时就过牌)\n\n\
出牌示例: [出 8910JQ]\n\
出牌解释: 牌型：顺子，牌组：[8,9,10,J,Q]\n\
牌的前后位置不影响牌组结构"
    output(info, Str)


def showMoveStoneGame(info):
    Str = "挪石头是一个简单的小游戏，需要两个玩家进行博弈，其规则如下：\n\
1.系统会给出两堆有一定数目的石头\n\
2.玩家可以设定一个正整数x，以及一个非负整数k\n\
3.玩家需要选择对哪堆进行操作，然后该堆会被扣除x，另一堆会被扣除kx\n\
4.两名玩家轮流操作，谁率先将两堆都清空，谁获胜。获胜者可以获得10积分，败者扣除10积分\n\
指令如下:\n\
[加入挪石头]\n\
[A x k]\n\
[B x k]\n\
[挪石头对局信息]\n\
[挪石头投降](主动投降也许可以少扣点积分)\n\
[挪石头掀桌]((玩家长时间未操作，任意群成员可掀桌))\n\
[开始人机挪石头](单人游戏,可私聊操作)\n\
[人机挪石头对局信息]\n\
[人机挪石头投降]\n\
示例:[A 5 7]\n\
解释:从A堆挪走5个石头，从B堆挪走5*7=35个石头"
    output(info, Str)


def showGameList(info):
    Str = "游戏列表:\n\
挪石头\n\
斗地主"
    output(info, Str)


def showServiceForCustomers(info):
    Str = "\
支持的操作列表：\n\
[查询cf比赛](用于查看最近的比赛列表)\n\
[cf昵称 昵称](用于绑定自己的昵称)\n\
[查询个人cf](用于查询个人的CF信息)\n\
[开启cf比赛提醒](每天中午检测CF比赛，当天有比赛时会私聊提醒，建议添加机器人为好友以免影响使用)\n\
[关闭cf比赛提醒]"
    output(info, Str)


#   发送反馈信息到开发组群
def sentFeedBackMessage(info, Str):
    info.autoBot.send_group_msg(
        261925581,
        Str
    )
    if info.autoImage is not None:
        info.autoBot.send_group_msg(
            261925581,
            msg=[
                miraicle.Image.from_id(info.autoImage.image_id)
            ]
        )


def showFeedBackSystem(info):
    Str = "\
反馈系统是一项用于向机器人开发组反馈意见的功能。\n\
如果使用者在使用机器人的过程中发现了程序的一些错误,\n\
或者是有什么想法以及改进建议，都可以通过反馈系统将\n\
建议发送到机器人开发组。并且反馈是匿名的。这意味着开发人员不会看到有关于您的个人信息\n\
指令如下:\n\
[反馈 内容]\n\
注：你可以附带一张图片放在内容末端，图片将会发送到开发组"
    output(info,  Str)


def showGroupRegulateSystem(info):
    Str = "\
群管系统是一项便捷辅助进行对群员执行操作的功能,\
本功能的使用前提是机器人在所在群拥有管理员权限。\
并且使用者需是机器人的管理人员，或者是群的管理人员\n\
具有如下指令:\n\
[禁言@某人(可以多个At) 时间(分钟,前面一定要有空格)]\n\
[解除禁言@某人(可以多个At)]\n\
[全体禁言]\n\
[解除全体禁言]\n\
[踢出@某人(可以多个At)]\n\
[添加违禁词 违禁词(可以多个,以空格隔开)]\n\
[删除违禁词 违禁词(可以多个,以空格隔开)]\n\
[违禁词列表]\n\
[清空违禁词]\n\
[刷屏限制 发言数]\n\
[开启违禁词禁言]\n\
[关闭违禁词禁言]\n\
[违禁词禁言时长 时间(单位：分钟)]\n\
[我信息呢](当你被机器人撤回消息时，可以发送看看)"
    output(info,  Str)


def showSetPersonalNick(info):
    output(info,  "请通过回复[设置昵称 新昵称]来更改你的昵称")


def showTeaRoomSystem(info):
    Str = f"\
茶馆系统是一个聊天系统\n\
使用者需要添加机器人为好友，双向添加成功后即可使用\n\
茶馆的某人发送消息，茶馆中所有人都会接收到。你可以通过发送[进入茶馆]或[离开茶馆]来更改你的状态。\n\
通过指令[茶馆 内容]来发送自己的消息。或者在开启便捷茶馆模式并且私聊情况下随意发送消息，它们都会被认作茶馆消息从而转发到茶馆中。\n\
也可以通过指令[茶馆在线列表]来查看当前茶馆中有多少人\n\
总结一下，就是6条指令:\n\
[进入茶馆]\n\
[离开茶馆]\n\
[茶馆 内容]\n\
[开启便捷茶馆]\n\
[关闭便捷茶馆]\n\
[茶馆在线列表]\n\
注:关闭便捷模式情况下你可以附带一张图片在消息末端，但是你所发的QQ表情将会无效\n\
而在便捷模式情况下，你所发的任QQ表情和图片都会严格按照原本的顺序和数目发送出去\n\
祝您使用愉快。"
    output(info,  Str)


def getPersonalScore(number):
    return userScore.get(str(number), 0)


def addPersonalScore(number, cnt):
    userScore[str(number)] = getPersonalScore(number) + cnt


def queryPersonalInformation(info):
    Str = f"\
--------个人信息--------\n\
QQ:{info.autoFriendNumber}\n\
昵称:{getName(info.autoFriendNumber)}\n\
是否为机器人管理员:{isAdmin(info.autoFriendNumber)}\n\
传话状态:{queryPassOnAMsgNumber(info.autoFriendNumber) != 0}\n\
拒绝别人传话:{getRefusePassOnAMsgState(info.autoFriendNumber)}\n\
茶馆状态:{getTeaState(info.autoFriendNumber)}\n\
茶馆便捷状态:{getTeaRoomAutoState(info.autoFriendNumber)}\n\
个人积分:{getPersonalScore(info.autoFriendNumber)}"
    output(info,  Str, True)


def queryTeaRoomOnlineList():
    Str = f"在线人数:{getTeaRoomPeopleNumber()}"
    for qq in teaRoomState:
        if qq != 'online' and teaRoomState.get(qq):
            Str += f"\n【{getName(qq)}({qq})】"
    return Str


def showMenu(info):
    menu = "\
      『   菜   单   』\n\
Ο设置昵称Ο反馈系统Ο\n\
Ο个人信息Ο便民工具Ο\n\
Ο茶馆系统Ο娱乐系统Ο\n\
Ο群管系统Ο积分排行Ο\n\
Ο传话系统Ο等待开发Ο"
    output(info,  menu)


def getRefusePassOnAMsgState(number):
    return refusePassOnAMsgState.get(str(number), False)


def setRefusePassOnAMsgState(number, sign):
    refusePassOnAMsgState[str(number)] = sign


def getTeaState(number):
    return teaRoomState.get(str(number), False)


def sentTeaRoomMessage(info, Str):
    for qq in teaRoomState:
        if getTeaState(qq) and qq != "online":
            jsonData = info.autoBot.send_friend_msg(
                            int(qq),
                            msg=[
                                miraicle.Plain(
                                    f"[online:{getTeaRoomPeopleNumber()}]茶馆[{st}]\n来自【{getName(info.autoFriendNumber)}(QQ:{info.autoFriendNumber})】的信息：\n"),
                                miraicle.MiraiCode(Str),
                            ]
                        )
            if jsonData.get('msg', 'None') == 'success':
                continue
            for groupNum in groupList:
                jsonData = info.autoBot.send_temp_msg(
                                groupNum,
                                int(qq),
                                msg=[
                                    miraicle.Plain(
                                        f"[online:{getTeaRoomPeopleNumber()}]茶馆[{st}]\n来自【{getName(info.autoFriendNumber)}(QQ:{info.autoFriendNumber})】的信息：\n"),
                                     miraicle.MiraiCode(Str),
                                ]
                             )
                if jsonData.get('msg', 'None') == 'success':
                    break


def showPassOnAMsg(info):
    Str = f"\
【该功能只能在私聊页面下触发】如果你有什么想对某人说的，但是又不想直接跟对方说，或者是还没添加对方为好友，则可以通过机器人来试试传话哦~\n\
前提是你得提供对方的QQ号，机器人会竭尽全力帮你传话的。\n\
你需要先通过指令[开始传话 对方QQ]来锁定传话的对象，之后你所发的任何消息，包括图片，表情，文字，机器人都会尽力传给对方。\n\
想要结束传话模式，输入指令[结束传话]就可以了哦~，如果不想被别人传话，可以发送[拒绝被传话]\n\
总结，4条指令：\n\
[开始传话 对方QQ]\n\
[结束传话]\n\
[允许被传话]\n\
[拒绝被传话]"
    output(info, Str)


def sentMsgToSomeOne(info, qq, Str):
    jsonData = info.autoBot.send_friend_msg(
                    int(qq),
                    msg=[
                        miraicle.Plain(
                            f"【{getName(info.autoFriendNumber)}(QQ:{info.autoFriendNumber})】让我帮忙传句话：\n"),
                        miraicle.MiraiCode(Str),
                    ]
                )
    if jsonData.get('msg', 'None') == 'success':
        return True
    for groupNum in groupList:
        jsonData = info.autoBot.send_temp_msg(
            groupNum,
            int(qq),
            msg=[
                miraicle.Plain(
                    f"【{getName(info.autoFriendNumber)}(QQ:{info.autoFriendNumber})】让我帮忙传句话：\n"),
                miraicle.MiraiCode(Str),
            ]
        )
        if jsonData.get('msg', 'None') == 'success':
             return True
    return False


def setTeaRoomState(number, state):
    teaRoomState[str(number)] = state
    if state:
        teaRoomState["online"] = getTeaRoomPeopleNumber() + 1
    else:
        teaRoomState["online"] = getTeaRoomPeopleNumber() - 1


def getTeaRoomPeopleNumber():
    return teaRoomState.get("online", 0)


#   获取用户在机器人程序中的昵称
def getName(number: str):
    return name.get(str(number), "无名氏")


#   设置用户在机器人程序中的昵称
def setName(info, Str):
    name[str(info.autoFriendNumber)] = Str


#   判断发言人是不是机器人的管理员
def isAdmin(number):
    return admin.get(str(number), False)


def updateTime():
    global st
    st = time.strftime("%H:%M:%S", time.localtime())


#   回复信息
def output(info,  Str, needAt=False, topImg=None, personal=False, newQQ=0):
    aimQQ = info.autoFriendNumber
    if newQQ != 0:
        aimQQ = newQQ
    if topImg is not None:
        if not info.isFriend and not personal:
            if needAt:
                info.autoBot.send_group_msg(
                    info.autoGroupNumber,
                    msg=[
                        miraicle.At(info.autoFriendNumber),
                        miraicle.Plain("\n"),
                        topImg,
                        miraicle.MiraiCode(f"{Str}")
                    ]
                )
            else:
                info.autoBot.send_group_msg(
                    info.autoGroupNumber,
                    msg=[
                        topImg,
                        miraicle.MiraiCode(f"{Str}")
                    ]
                )
        else:
            if info.autoBot.send_friend_msg(
                    aimQQ,
                    msg=[
                        topImg,
                        miraicle.MiraiCode(Str)
                    ]
            ).get('msg', 'None') == 'success':
                return
            for groupNum in groupList:
                jsonData = info.autoBot.send_temp_msg(
                    groupNum,
                    int(aimQQ),
                    msg=[
                        topImg,
                        miraicle.MiraiCode(Str)
                    ]
                )
                if jsonData.get('msg', 'None') == 'success':
                    return
    else:
        if not info.isFriend and not personal:
            if needAt:
                info.autoBot.send_group_msg(
                    info.autoGroupNumber,
                    msg=[
                        miraicle.At(aimQQ),
                        miraicle.Plain("\n"),
                        miraicle.MiraiCode(f"{Str}")
                    ]
                )
            else:
                info.autoBot.send_group_msg(
                    info.autoGroupNumber,
                    msg=[
                        miraicle.MiraiCode(f"{Str}")
                    ]
                )
        else:
            if info.autoBot.send_friend_msg(
                    aimQQ,
                    msg=[
                        miraicle.MiraiCode(Str)
                    ]
            ).get('msg', 'None') == 'success':
                return
            for groupNum in groupList:
                print(groupNum)
                jsonData = info.autoBot.send_temp_msg(
                    groupNum,
                    int(aimQQ),
                    msg=[
                        miraicle.MiraiCode(Str)
                    ]
                )
                if jsonData.get('msg', 'None') == 'success':
                    return


def getAllAtQQ(jsonInfo):
    allAtQQ = []
    msgChain = jsonInfo.get('messageChain', None)
    for dic in msgChain:
        if dic.get('type', None) == 'At':
            allAtQQ.append(dic.get('target', None))
    return allAtQQ


def getFullMsgInfo(jsonInfo):
    Str = ""
    msgChain = jsonInfo.get('messageChain', None)
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


def addAdministrator(number):
    admin[str(number)] = True


def deleteAdministrator(number):
    admin[str(number)] = False


def addMsgMatch(Str1, Str2):
    msgMatch[Str1] = Str2


def setTeaRoomAutoState(number, sign):
    teaRoomAutoState[str(number)] = sign


def getTeaRoomAutoState(number):
    return teaRoomAutoState.get(str(number), False)


#   游戏区


def changeScore(changeList):
    for qq in changeList:
        addPersonalScore(qq, changeList[qq])


def getScoreChangeInfo(changeList):
    Str = "用户积分变更情况:"
    for qq in changeList:
        Str += f"\n【{getName(qq)}】({qq}):{changeList[qq]}"
    return Str


#   挪石头
def runningMoveStoneGame(info: _Info):
    # if re.match(info.autoPlain, "")
    if groupMoveStone.get(info.autoGroupNumber, None) is None:
        groupMoveStone[info.autoGroupNumber] = MoveStoneGame.MoveStone()
    Dict = groupMoveStone[info.autoGroupNumber].running(info.autoFriendNumber, info.autoPlain)
    # print(Dict)
    if Dict.get("breakGame", False):
        output(info, "有人掀桌，挪石头游戏已重置！")
        changeScore(Dict.get("scoreChangeList", {}))
        output(info, getScoreChangeInfo(Dict.get("scoreChangeList", {})))
        groupMoveStone[info.autoGroupNumber].reset()
        return
    if Dict.get("active", False) is False:
        return
    if Dict.get("legal", False) is False:
        output(info, Dict.get("errorBack", ""), True)
        return
    output(info, Dict.get("normalBack", ""), True)
    if Dict.get("state", "waiting") == "running" and not Dict.get("finish", False):
        output(info, f"{Dict.get('gameInfo', '')}")
        output(info, f"接下来轮到玩家【{getName(Dict.get('nowOperator', 0))}】({Dict.get('nowOperator', 0)})执行操作")
    if Dict.get("finish", False):
        output(info, f"恭喜玩家【{getName(Dict.get('winner', 0))}】获得胜利！\n")
        changeScore(Dict.get("scoreChangeList", {}))
        output(info, getScoreChangeInfo(Dict.get("scoreChangeList", {})))
        groupMoveStone[info.autoGroupNumber].reset()


#   挪石头人机模式
def runningMoveStoneGameBotModel(info: _Info):
    # if re.match(info.autoPlain, "")
    if personalMoveStone.get(info.autoFriendNumber, None) is None:
        personalMoveStone[info.autoFriendNumber] = MoveStoneGameBotModel.MoveStoneBotModel()
    Dict = personalMoveStone[info.autoFriendNumber].running(info.autoFriendNumber, info.autoPlain)
    # print(Dict)
    if Dict.get("active", False) is False:
        return
    if Dict.get("legal", False) is False:
        output(info, Dict.get("errorBack", ""), not info.isFriend)
        return
    output(info, Dict.get("normalBack", ""), not info.isFriend)
    if Dict.get("state", "waiting") == "running" and not Dict.get("finish", False):
        output(info, f"{Dict.get('gameInfo', '')}")
        output(info, f"接下来轮到玩家【{getName(Dict.get('nowOperator', 0))}】({Dict.get('nowOperator', 0)})执行操作")
    if Dict.get("finish", False):
        output(info, f"恭喜玩家【{getName(Dict.get('winner', 0))}】获得胜利！\n")
        changeScore(Dict.get("scoreChangeList", {}))
        output(info, getScoreChangeInfo(Dict.get("scoreChangeList", {})))
        personalMoveStone[info.autoFriendNumber].reset()


#   斗地主
def runningFightTheLandlordGame(info: _Info):
    if groupFightTheLandlord.get(info.autoGroupNumber, None) is None:
        groupFightTheLandlord[info.autoGroupNumber] = FightTheLandlordGame.FightTheLandlord()
    Dict:dict = groupFightTheLandlord[info.autoGroupNumber].running(info.autoFriendNumber, info.autoPlain)
    if not Dict.get("active", False):
        return
    if Dict.get("breakGame", False):
        output(info, "有人掀桌！游戏状态已重置！对局玩家受到对应奖惩")
        changeScore(Dict.get("scoreChangeList", {}))
        output(info, getScoreChangeInfo(Dict.get("scoreChangeList", {})))
        groupFightTheLandlord[info.autoGroupNumber].reset()
        return
    if Dict.get("finish", False):
        output(info, f"对局结束！获胜方:{Dict.get('winner', 'None')}")
        Str = ""
        for qq in Dict.get("playerArr", []):
            tempStr = groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(qq)
            if tempStr != "":
                Str += f"玩家【{getName(qq)}】({qq})剩余的牌:\n{tempStr}\n"
        output(info, Str)
        changeScore(Dict.get("scoreChangeList", {}))
        output(info, getScoreChangeInfo(Dict.get("scoreChangeList", {})))
        groupFightTheLandlord[info.autoGroupNumber].reset()
        return
    if not Dict.get("legal", False):
        output(info, Dict.get("errorBack", ""))
        if Dict.get("errorBack", "") == "玩家查询牌信息，已将牌再次发送给玩家":
            output(info, f"你的牌:\
                            \n{groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(info.autoFriendNumber)}",
                   personal=True)
            return
        if Dict.get("errorBack", "") == "玩家明牌":
            output(info, f"【{getName(info.autoFriendNumber)}】({info.autoFriendNumber})的牌:\
            \n{groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(info.autoFriendNumber)}")
        if Dict.get("errorBack", "") == "玩家叫地主":
            qq = Dict.get("nowOperator", 0)
            output(info, f"接下来轮到【{getName(qq)}】({qq})进行操作")
        if Dict.get("errorBack", "") == "无人叫地主":
            output(info, "由于无人叫地主，已重新发牌")
            for qq in Dict.get("playerArr", []):
                output(info, f"你的牌:\n{groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(qq)}"\
                       , personal=True, newQQ=qq)
            qq = Dict.get("nowOperator", 0)
            output(info, f"接下来轮到【{getName(qq)}】({qq})进行操作\n叫地主环节,发送[叫地主]或[不叫]")
            return
        if Dict.get("errorBack", "") == "叫地主结束":
            landlord = Dict.get("landlord", 0)
            output(info, f'玩家【{getName(landlord)}】({landlord})成为地主！\n地主牌:\
{groupFightTheLandlord[info.autoGroupNumber].queryLandlordPoker()}')
            output(info, f"你的牌:\n{groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(landlord)}"\
                   , personal=True, newQQ=landlord)
            output(info, "接下来请地主出牌\n出牌示例:[出 910JQK]\n示例解释:  牌型:顺子,牌组:[9,10,J,Q,K]\n要不起请发送[过]")
            return
        if Dict.get("errorBack", "") == "玩家不叫":
            qq = Dict.get("nowOperator", 0)
            output(info, f"接下来轮到【{getName(qq)}】({qq})进行操作")
    else:
        output(info, Dict.get("normalBack", ""))
        if Dict.get("state", "") == "对局中":
            if groupFightTheLandlord[info.autoGroupNumber].queryLightPoker(info.autoFriendNumber):
                output(info, f"【{getName(info.autoFriendNumber)}】({info.autoFriendNumber})的牌:\
                \n{groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(info.autoFriendNumber)}")
            output(info, f"你的牌:\
                \n{groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(info.autoFriendNumber)}", personal=True)
            qq = Dict.get("nowOperator", 0)
            output(info, f"接下来轮到【{getName(qq)}】({qq})进行操作")
            return
        if Dict.get("state", "") == "叫地主":
            qq = Dict.get("nowOperator", 0)
            output(info, f"接下来轮到【{getName(qq)}】({qq})进行操作\n叫地主环节,发送[叫地主]或[不叫]")
            for qq in Dict.get("playerArr", []):
                output(info, f"你的牌:\n{groupFightTheLandlord[info.autoGroupNumber].queryPokerInfo(qq)}"\
                       , personal=True, newQQ=qq)
            return


robotQQ = 1784518480
port = 8080
verify_code = '114514'
bot = miraicle.Mirai(robotQQ, verify_code, port)  # adapter='ws' 参数更改 websocket/http
bot.run()
