import requests
import sys
from bs4 import BeautifulSoup
import datetime as dt
import os

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

# 5) 뉴스 기사들 수집
# 뉴스기사의 내용들을 누적해서 저장하기 위한 빈 문자열 변수
content_merge = ""

# 리스트 목록만큼 반복
for i, url in enumerate(url_list) :
    print('%d번째 뉴스기사 수집중... >>\n' %(i+1), url)
    # 1) html 소스 가져오기
    r = requests.get(url, headers=headers)
    
    if r.status_code != 200 :
        print('[ERROR] %s' %r.status_code)
        continue

    # 2) 기사 영역 추출하기
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(r.text, 'html.parser')
    # 제목+본문을 감싸는 태그 추출
    selector = soup.select('.newsct')
    #print(selector)
    #print('-' * 20)
    #print(len(selector))
    #print('-' * 20)

    # 3) 제목 추출 : 파일명으로 사용
    title = selector[0].select('#title_area')
    #print(title)
    
    title_str = title[0].text.strip();
    #print(title_str)
    #print('-' * 20)
    # 파일명으로 사용할 수 없는 문자 제거
    title_str = title_str.replace('"', '')  # 큰따옴표
    title_str = title_str.replace('\\', '') # 역슬래시
    title_str = title_str.replace('/', '')  # 슬래시
    title_str = title_str.replace('?', '')  # 물음표
    title_str = title_str.replace('>', '')  # 꺽기 괄호
    title_str = title_str.replace('<', '')  # 꺽기 괄호
    title_str = title_str.replace('*', '')  # 별문자
    title_str = title_str.replace('|', '')  # 긴줄 문자
    title_str = title_str.replace(':', '')  # 콜론
    # 둥근따옴표 => 'ㄴ' -> 한자 클릭 -> 둥근따옴표 선택
    title_str = title_str.replace('“', '') 
    title_str = title_str.replace('”', '') 
    #print(title_str)
    
    # 4) 본문 추출
    article = selector[0].select('#dic_area')
    #print(article)
    
    # 불필요한 태그 제거 및 치환
    article_item = article[0]
    
    for target in article_item.select('.end_photo_org') :
        target.extract()
        
    for target in article_item.select('strong') :
        target.extract()
    
    for target in article_item.select('br') :
        target.replace_with('\n')
        
    #print(article_item)
    # 본문 텍스트 추출
    article_str = article_item.text.strip()
    #print(article_str)
    
    # 문자열 변수에 기사 누적시키기
    content_merge += article_str
    print('-' * 20)

#print(content_merge)
#print('-' * 20)

# 2. 워드클라우드
from collections import Counter  # 빈도수 분석 모듈
from wordcloud import WordCloud
from konlpy.tag import Okt       # 한글 형태소 분석 모듈

# 1) 명사 추출
nlp = Okt()
nouns = nlp.nouns(content_merge)
#print(len(nouns))
#print(nouns[:100])
#print('-' * 20)

# 2) 한글자 단어 제거
for i, v in enumerate(nouns) :
    if len(v) < 2 :
        nouns.remove(v)
        #del(nouns[i])
        
#print(len(nouns))
#print(nouns[:100])
#print('-' * 20)

# 3) 중요하지 않은 단어 제거
remove_list = ['기자','것','상대로','심','지난','이것']
for n in nouns :
    if n in remove_list :
        nouns.remove(n)

#print(len(nouns))
#print(nouns[:100])
#print('-' * 20)

# 4) 단어별 빈도수 검사
count = Counter(nouns)
#print(count)
#print('-' * 20)
#print(len(count))
#print('-' * 20)

# 5) 상위 50건 추출
most = count.most_common(50)
#print(most)
#print('-' * 20)

# 6) 워드클라우드에서 사용할 데이터 형식으로 변경
# 튜플로 구성된 리스트 => 딕셔너리
tags = {}
for n, c in most :
    tags[n] = c

#print(tags)
#print('-' * 20)

# 7) 워드클라우드 생성
wc = WordCloud(font_path='data/NanumBarunGothic.ttf',
               width=1200, height=600, background_color='white')
# 8) 워드클라우드 그래프 생성
wc.generate_from_frequencies(tags)

# 9) 그래프 출력
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 12))
plt.imshow(wc)
plt.axis('off')   # 그래프창 테두리 없애기
plt.show()

# 10) 그래프를 파일로 저장
wc.to_file('news.png')
print('저장 성공')







