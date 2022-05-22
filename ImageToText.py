from gettext import gettext
import requests
stk = 0

def getTextFromImage(imageUrl):
    global stk
    url = 'http://localhost:8089/api/tr-run/'
    r = requests.get(imageUrl)
    stk += 1
    with open(f"t{stk}.jpg", 'wb') as f:
        f.write(r.content)
    stk -= 1
    img1_file = {
        'file': open(f't{stk+1}.jpg', 'rb')
    }
    res = requests.post(url=url, data={'compress': 0}, files=img1_file).json().get('data',{})
    temp = res.get('raw_out', [])
    Str = ""
    for List in temp:
        Str += List[1]
    ret = ""
    List = Str.split()
    for s in List:
        ret += s
    return ret

if __name__ == '__main__':
    str = getTextFromImage("http://gchat.qpic.cn/gchatpic_new/1924645279/4151925581-2468997682-C486F1E977349DCFC79119CF62865EF7/0?term=2")
    print(str)