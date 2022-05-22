import requests
url = 'http://localhost:8089/api/tr-run/'
img1_file = {
    'file': open('1.jpg', 'rb')
}
res = requests.post(url=url, data={'compress': 0}, files=img1_file).json().get('data',{})
temp = res.get('raw_out', [])
Str = ""
for List in temp:
    Str += List[1]
print(Str)
