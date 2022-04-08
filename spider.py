import requests
from requests.packages import urllib3
import json
import time

Path = ".\\output\\output.txt"
urllib3.disable_warnings()


def getCodeForcesContestInfo():
  temp = requests.get("https://zhuanlan.zhihu.co", verify=False)
  print(temp)
  response = temp.json()
  sign = False
  if response.get('status', 'FAILED') == 'FAILED':
    return "获取信息失败..."
  else:
    sign = True
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
      Str += f"比赛时间:{'%04d' % ti.tm_year}-{'%02d' % ti.tm_mon}-{'%02d' % (ti.tm_mday + int((ti.tm_hour + 8) / 24))} {'%02d' % int((ti.tm_hour + 8) % 24)}:{'%02d' % ti.tm_min}:{'%02d' % ti.tm_sec}\n"
      temp = dic.get('durationSeconds', 0)
      Str += f"比赛时长: {'%02d' % int(temp / 3600)}:{'%02d' % int((temp % 3600) / 60)}:{'%02d' % int(temp % 60)}\n"
      Max -= 1
      if not Max:
        break
    if Str == "CF近期比赛列表(5天内):":
      Str += "\n近期暂无比赛..."
    return Str



if __name__ == '__main__':
  getCodeForcesContestInfo()
