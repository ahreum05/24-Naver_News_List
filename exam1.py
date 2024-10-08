import requests
import sys
from bs4 import BeautifulSoup

url = 'https://news.naver.com/main/ranking/popularDay.naver'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
headers = {'User-Agent': user_agent, 'Referer': None}

r = requests.get(url, headers=headers)

if r.status_code != 200 :
    print('[ERROR] %s' %r.status_code)
    sys.exit(0)
    
#print(r.text)
print('-' * 20)

# 1) BeautifulSoup 객체 생성
soup = BeautifulSoup(r.text, 'html.parser')

# 2) <a> 태그만 추출
selector = soup.select('.rankingnews_box_wrap  .rankingnews_list .list_title')
print(selector)
print('-' * 20)
print(len(selector))
print('-' * 20)

# 3) url 수집
# <a href="url">
url_list = []    # url을 저장할 리스트

# item.attrs : 태그의 속성 읽기
for item in selector :
    if 'href' in item.attrs : 
        url_list.append(item['href'])

print(url_list)
print('-' * 20)




