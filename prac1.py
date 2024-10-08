import requests
import sys
from bs4 import BeautifulSoup
import datetime as dt
import os # 파일 만들고 저장하는 클래스

url = 'https://news.daum.net/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
headers = {'User-Agent' : user_agent, 'Referer': None}

r = requests.get(url, headers=headers)

if r.status_code != 200 :
    print('[ERROR] %s' %r.status_code)
    sys.exit(0)
    
#print(r.text)
print('-' * 20)

# BeautifulSoup 객체 생성
soup = BeautifulSoup(r.text, 'html.parser')

# 1. <a>태그의 url 추출
# 1) <a> 태그만 추출
selector = soup.select('.item_issue .link_txt')
#print(selector)
#print('-' * 20)
#print(len(selector))
#print('-' * 20)

# 2) url 수집
# <a herf="url">
url_list = []   # url을 저장할 리스트

# item.attrs : 태그의 속성 읽기
for item in selector :
    if 'href' in item.attrs :
        url_list.append(item['href'])

#print(url_list)
#print('-' * 20)

# 2. 수집된 기사들을 저장할 폴더 생성
# 현재 시간 저장하기
date_str = dt.datetime.now().strftime('%y%m%d_%H%M%S')
dir_name = '다음뉴스기사_' + date_str
# 폴더 만들기
if not os.path.exists(dir_name) :
    os.mkdir(dir_name)

# 3. 기사 추출 : 제목 + 본문
# 리스트 목록만큼 반복
for i, url in enumerate(url_list):
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
    selector = soup.select('#mArticle')
    #print(selector)
    #print('-' * 20)
    #print(len(selector))
    #print('-' * 20)

    # 3) 기사 제목 추출 : 파일명으로 사용
    title = selector[0].select('.tit_view')
    #print(title)
    
    title_str = title[0].text.strip();
    #print(title_str)

    # 파일명으로 사용할 수 없는 문자 제거
    title_str = title_str.replace('"', '')    #큰따옴표
    title_str = title_str.replace('\\', '')   #역슬래시
    title_str = title_str.replace('/', '')    #슬래시
    title_str = title_str.replace('?', '')    #물음표
    title_str = title_str.replace('>', '')    #꺽기괄호
    title_str = title_str.replace('<', '')    #껵기괄호
    title_str = title_str.replace('*', '')    #별문자
    title_str = title_str.replace('|', '')    #긴줄문자
    title_str = title_str.replace(':', '')    #콜론
    # 둥근따옴표 => 'ㄴ' => 한자 클릭 => 둥근따옴표 선택
    title_str = title_str.replace('“', '')
    title_str = title_str.replace('”', '')
    #print(title_str)

    # 4) 본문 추출
    article = selector[0].select('.article_view section')
    #print(article)
    
    # 불필요한 태그 제거 및 치환
    article_item = article[0]
    
    for target in article_item.select('figure') :
        target.extract()
        
    #print(article_item)

    # 본문 텍스트 추출
    article_str = article_item.text.strip()
    #print(article_str)

    # 5) 제목과 내용을 텍스트 파일로 저장
    if title_str and article_str : 
        fname = dir_name + '/' + str(i+1) + "_" + title_str + '.txt'
        
        with open(fname, 'w', encoding='utf-8') as f :
            f.write(article_str)
            print(' >> 파일 저장 성공 :', fname)
    
    print('-' * 20)

        
        
        
        
    
    
