import requests
url = 'http://localhost:8089/api/tr-run/'
img1_file = {
    'file': open('114.jpg', 'rb')
}
res = requests.post(url=url, data={'compress': 0}, files=img1_file)
print(res)
def getTextFromImage(path):
    url = 'http://localhost:8089/'
    file = {
        'file': open(path)
    }
    res = requests.post(url=url, data={'compress': 0}, files=img1_file).json()
    Str = ""
    