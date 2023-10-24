import requests
from time import sleep

url_login = 'http://193.20.1.2:5000/login'
url_search = 'http://193.20.1.2:5000/search?name='
payload = {'nome': 'guest', 'pass': 'guest'}

p = ['apple', 'watermelon', 'banana']
i = 0

sleep(30)
    
s = requests.Session()
x = s.post(url_login, data=payload)

while True:
    x = s.get(url_search + str(p[i]))
    
    i += 1
    if i >= 3:
        i = 0
    
    sleep(60)
