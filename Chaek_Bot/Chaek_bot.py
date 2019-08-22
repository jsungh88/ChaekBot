# -*- coding: utf-8 -*-
import json
import requests
from flask import Flask, request, Response
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from openpyxl import load_workbook
import random
import os

##기본정보
API_KEY = '[API_KEY]' #챗봇API(Cheack_bot)
app = Flask(__name__)
url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage


#받은메시지정보: 유저 Id, 유저이름, 메시지 가져오기 
def parse_message(data): #메시지 가져와서 id, msg 추출
    print("**********************")
    print("[PARSE_MESSAGE]:",data)
    print("**********************")
    chat_id = data['message']['chat']['id']
    last_name = data['message']['chat']['last_name']
    msg = data['message']['text']
    print(chat_id, last_name, msg)    
    
    return chat_id, last_name, msg

#인사말 보내기 : '도서검색','도서추천'메뉴를 보여준다. 
def send_hello(chat_id, last_name, text='인사말입니다.'):
    print("**********************************")
    print("[SEND_HELLO]:",chat_id,last_name,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {
            'keyboard':[[{
                    'text': '도서 검색'
                        },
                    {'text': '도서 추천'
                        }]
                    ],
            'one_time_keyboard' : True
            } 
    text = '<i>Cheak!(췍!) Cheak!(췍!)...</i> \r\n "<b>{이름}</b>"님, 안녕하세요!😄 저는 여러분들이 원하는 책을 쉽게 찾아드리는 <b>"책봇(Cheak Bot)"</b> 입니다.😊📚\r\n\r\n<b> 도서검색, 도서추천(베스트셀러/장르별/기분별)서비스</b> 이용하고, 원하는 책을 편하고 친숙하게 추천 받아보세요.🙌\r\n\r\n 어떤 방법으로 책을 Cheak(췌크)해 볼까요?'.format(이름=last_name)    
    params = {'chat_id':chat_id, 'text': text, 'parse_mode':'HTML', 'reply_markup' : keyboard} #Markdown or HTML 
    response = requests.post(url, json=params)   
    
    return 0

# '도서검색'메뉴 선택: 사용자가 '도서검색'메뉴를 선택하면, 챗봇은 '검색어를 입력해달라'는 메시지를 보내준다. 
def send_search(chat_id, text='검색중입니다.'):
    print("**********************************")
    print("[SEND_SEARCH]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {
            'keyboard':[[{
                    'text': '메뉴로 이동'
                        }]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }
    message = '검색어(도서명,저자명,출판사 등)를 입력해주세요. 검색어 앞에는 ">"를 붙여주세요.😄\r\n (예시: >공부머리 독서법)'
    params = {'chat_id':chat_id, 'text':message,'reply_markup' : keyboard }
    response = requests.post(url, json=params)   
    
    return 0

# 메뉴화면으로 돌아가겠냐는 의사를 묻는 메소드: 
# '메뉴로 돌아가시겠어요?'라는 메시지가 뜨고,  '메뉴'버튼을 선택하면, 메뉴버튼이 보여진다.(back메소드로 연결.) - 어쩌면 불필요한 depth. 수정 필요.
def back(chat_id, text='메뉴로 버튼'):
    print("**********************************")
    print("[BACK]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{
                    'text': '메뉴'
                        }]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            } 
    params = {'chat_id':chat_id, 'text': '메뉴로 돌아가시겠어요?😄', 'reply_markup' : keyboard} #Markdown or HTML 
    response = requests.post(url, json=params)
    return 0 

# 메뉴(도서검색/도서추천)버튼 보여주기
def menu(chat_id, text):
    print("**********************************")
    print("[MENU]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{
                    'text': '도서 검색'
                        },
                    {'text': '도서 추천'
                        }]
                    ],
            'one_time_keyboard' : True,
            } 
    
    params = {'chat_id':chat_id, 'text': text, 'reply_markup' : keyboard} #Markdown or HTML 
    response = requests.post(url, json=params)   
    return 0 
    
#아직 의미없는 메소드. 
def send_message(chat_id, text='대화시도'):
    print("**********************************")
    print("[SEND_MESSAGE]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    params = {'chat_id':chat_id, 'text': text }
    response = requests.post(url, json=params)    
    
    return 0

# '도서검색'하기: 's'+도서정보(도서명,저자명,출판사 등)를 입력하면, 해당 도서정보를 찾아 메시지로 전송한다.
def search_book(chat_id, text='도서검색'):  
    print("**********************************")
    print("[SEARCH_BOOK]:",chat_id,text)
    print("**********************************")
    
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    #검색결과 저장할 변수
    title_list = []
    image_list = []
    author_list = []
    publisher_list = []
    link_list = []
    desc_list = []
    title_list, image_list, author_list, publisher_list, link_list, desc_list = getSearchResult(text) #★getSearchResult를 통해, 도서정보list(제목,저자명,출판사,설명,링크)를 불러온다. 
    """text
    print("title_list:",title_list)
    print("image_list:",image_list)
    print("author_list:",author_list)
    print("publisher_list:",publisher_list)
    print("link_list:",link_list)
    print("desc_list:",desc_list)    
    
    book_info = dict(zip(title_list,author_list)) #책제목과 작가명을 매칭시킨 딕셔너리 생성.
    print('dic:',book_info)
    """
    #getSearchResult를 통해 받아온 도서정보리스트(제목list,저자list,이미지list,출판사list,링크list,설명list)를
    #모두 하나의 텍스트변수(book_info)로 묶어서, 그 book_info를 유저에게 메시지를 전송한다.  
    if len(title_list) < 5:
        for i in range(len(title_list)):
            title = title_list[i]
            author = author_list[i]
            image = image_list[i]
            publisher = publisher_list[i]
            link = link_list[i]
            description = desc_list[i]
            book_info = "이미지:{image}    도서명:<b>{title}</b> \r\n    작가명:<b>{author}</b>    출판사:<b>{publisher}</b>    설명:{description}    링크:{link}".format(image=image, title=title, author = author, publisher = publisher, description = description, link = link)
            print("book_info:",book_info)
            params = {'chat_id':chat_id, 'text': book_info, 'parse_mode':'HTML'}
            response = requests.post(url, json=params)
            print("response:",response)
        
    else:
        for i in range(5):
            title = title_list[i]
            author = author_list[i]
            image = image_list[i]
            publisher = publisher_list[i]
            link = link_list[i]
            description = desc_list[i]
            book_info = "이미지:{image}    도서명:<b>{title}</b> \r\n    작가명:<b>{author}</b>    출판사:<b>{publisher}</b>    설명:{description}    링크:{link}".format(image=image, title=title, author = author, publisher = publisher, description = description, link = link)
            print("book_info:",book_info)
            params = {'chat_id':chat_id, 'text': book_info, 'parse_mode':'HTML'}
            response = requests.post(url, json=params)
            print("response:",response)
    

    #검색결과를 모두 보여준 후, 메뉴로 돌아가겠냐는 의사를 묻는 메소드.          
    #back(chat_id, '뒤로')
    #send_search(chat_id, '도서 검색')
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    message = '검색어(도서명,저자명,출판사 등)를 입력해주세요.😄 검색어 앞에는 ">"를 붙여주세요.\r\n (예시: >공부머리 독서법)\r\n메뉴로 돌아가려면 "메뉴"를 입력하세요.🙂'
    params = {'chat_id':chat_id, 'text':message}
    response = requests.post(url, json=params)   
    
    return 0

    

#도서정보를 naverAPI로부터 불러오는 메소드.
def getSearchResult(keyword):
    print("**********************************")
    print("[GETSEARCHRESULT]: 도서검색결과",keyword)
    print("**********************************")
    
    CLIENT_ID = 'NaverAPI_KEY'
    CLIENT_SECRET = 'OeVF11yjte'
    
    request = Request('https://openapi.naver.com/v1/search/book?query='+quote(keyword))
    request.add_header('X-Naver-Client-Id', CLIENT_ID)
    request.add_header('X-Naver-Client-Secret', CLIENT_SECRET)      
    response = urlopen(request).read().decode('utf-8')
    
    search_result = json.loads(response)
    #print('keyword:',search_result)
    
    title_list = []
    image_list = []
    author_list = []
    publisher_list = []
    link_list = []
    desc_list = []
    
    for i in range(len(search_result['items'])):
        title = search_result['items'][i]['title']
        image = search_result['items'][i]['image']
        author = search_result['items'][i]['author']
        publisher = search_result['items'][i]['publisher']
        description = search_result['items'][i]['description']
        link = search_result['items'][i]['link']
        print("title,image,author,publisher,description,link",title,image,author,publisher,description,link)
        
        #문제: <b>,</b>태그때문에 검색결과가(response:400)으로  보내지지 않음.
        #해결1)title에서 <br> 또는 </br>제거
        if "<b>" in title or "</b>" in title:
            print("title_before",title)
            title = title.replace("<b>","")
            title = title.replace("</b>","")
            print("title_after",title)
            title_list.append(title)
        else:
            title_list.append(title)
            
        #해결)author에서 <br> 또는 </br>제거
        if "<b>" in author or "</b>" in author:
            print("author_before",author)
            author = author.replace("<b>","")
            author = author.replace("</b>","")
            print("author_after",author)
            author_list.append(author)
        else:
            author_list.append(author)
        
        #해결)publisher에서 <br> 또는 </br>제거
        if "<b>" in publisher or "</b>" in publisher:
            print("publisher_before",publisher)
            publisher = publisher.replace("<b>","")
            publisher = publisher.replace("</b>","")
            print("publisher_after",publisher)
            publisher_list.append(publisher)
        else:
            publisher_list.append(publisher)
        
        #해결)description에서 <br> 또는 </br>제거
        if "<b>" in description or "</b>" in description:
            print("description_before",description)
            description = description.replace("<b>","")
            description = description.replace("</b>","")
            print("description_after",description)
            desc_list.append(description)
        else:
            desc_list.append(description)
        
        #image,link는 그대로 저장.
        image_list.append(image)
        link_list.append(link)
        
        print("title_list",title_list)        
        print("author_list",author_list)
        print("publisher_list",publisher_list)
        print("desc_list",desc_list)
        print("image_list",image_list)
        print("link_list",link_list)
        
        
        
    #검색된 결과를 요소별(제목,이미지,저자,출판사,링크,설명)리스트로 묶어 반환한다. 
    return title_list, image_list, author_list, publisher_list, link_list, desc_list

# '도서추천'메뉴선택 시, 선택지를 보여준다 : 베스트셀러 or 장르별 or 감정별 중 선택 가능. 
def send_curate(chat_id, text ='도서 추천'):
    print("**********************************")
    print("[SEND_CURATE]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{'text':'베스트셀러'}],[{'text': '장르별'}],[{'text': '감정별'}]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }   
    
    if text == '베스트셀러':
        params = {'chat_id':chat_id, 'text': text, 'reply_markup' : keyboard}
        requests.post(url, json = params)
        
        return 0
    elif text == '장르별':
       
        params = {'chat_id':chat_id, 'text':text, 'reply_markup' : keyboard}
        requests.post(url, json = params)
        return 0
    elif text == '감정별':
       
        params = {'chat_id':chat_id, 'text':text, 'reply_markup' : keyboard}
        requests.post(url, json = params)
        return 0
    else:
        params = {'chat_id':chat_id, 'text':'어떤 서비스를 이용하시겠습니까?🧐', 'reply_markup' : keyboard}
        requests.post(url, json = params)
        return 0
    
    params = {'chat_id':chat_id, 'text': text, 'reply_markup' : keyboard}
    response = requests.post(url, json=params)    
    
    return 0

# '장르별 추천'기능:
# '장르별 추천'을 클릭하면, 카테고리 코드를 보여주고 사용자가 해당 코드를 입력하면
# 해당 도서중 아무거나 random으로 3권을 뽑아서 추천해주는 기능.  \r\n
def genre(chat_id, text='장르별 추천'):
    print("**********************************")
    print("[GENRE]:",chat_id,text)
    print("**********************************")
    
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{'text':'도서추천 방법 다시 선택'}],[{'text':'메뉴로 이동'}]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }   
    
    
    msg = '<b>[국내도서]</b> \r\n 소설 - code101 \r\n 시/에세이 - code102 \r\n 예술/대중문화 - code103\r\n사회과학 - code104\r\n역사와 문화 - code105\r\n잡지 - code107\r\n만화 - code108\r\n유아 - code109\r\n아동 - code110\r\n가정과 생활 - code111\r\n청소년 - code112\r\n초등학습서 - code113\r\n고등학습서 - code114\r\n국어/외국어/사전 - code115\r\n자연과 과학 - code116\r\n경제경영 - code117\r\n자기계발 - code118\r\n인문 - code119\r\n종교/역학 - code120\r\n컴퓨터/인터넷 - code122\r\n자격서/수험서 - code123\r\n취미/레저 - code124\r\n전공도서/대학교재 - code125\r\n건강/뷰티 - code126\r\n여행 - code128\r\n중등학습서 - code129\r\n\r\n<b>[외국도서]</b>\r\n어린이 - code201\r\nELT/사전 - code203\r\n문학 - code205\r\n경영/인문 - code206\r\n예술/디자인 - code207\r\n실용 - code208\r\n해외잡지 - code209\r\n대학교재/전문서적 - code210\r\n컴퓨터 - code211\r\n일본도서 - code214\r\n프랑스도서 - code215\r\n중국도서 - code216\r\n해외주문원서 - code217\r\n \r\n코드를 입력해주세요.<b>\r\n(예시: code101)</b> '
    print("text:",text)
    
    params = {'chat_id':chat_id, 'text': msg, 'parse_mode':'HTML', 'reply_markup' : keyboard}
    print("params:",params)
    response = requests.post(url, json=params)
    print("response:",response)
    
    return 0

#엑셀파일에서 {카테고리:code,...} 딕셔너리를 받아오는 메소드.
def getCategory(code):
    print("**********************************")
    print("[GETCATEGORY]:OK")
    print("**********************************")
    
    #엑셀파일(category_info.xlsx)에서 카테고리 ID 불러오기.
    EXCEL_FILE_NAME = 'category_info.xlsx'
    db = load_workbook(filename=EXCEL_FILE_NAME)
    category_db = db['카테고리정보']
    cate_dict = {}
    print("cate_dict:",cate_dict)
    
    #카테고리명과 해당 코드가 짝지어진 dictionary 만들기. 
    #cate_dict = {'코드명1':'카테고리명1','코드명2':'카테고리2',...} 
    for row in category_db.rows:
        if row[0].value is not None:
            cate_dict[row[0].value] = row[1].value
            
    return cate_dict
    

#유저가 도서 코드를 입력하면,  해당코드 장르의 도서정보를 랜덤으로 뿌려준다. 
def genreSearch(chat_id, code):
    print("**********************************")
    print("[GENRESEARCH]:",chat_id,code)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    
    #엑셀로부터 카테고리정보 dictionary를 불러온다. 
    cate_dict = {}
    cate_dict = getCategory(code)
    print("return_cate_dict:",cate_dict)
    print("cate_dict[code]:",cate_dict[int(code)]) #key값이 str로 들어가서 int로 변환해줌.
    
    cate_name = cate_dict[int(code)]
    print("cate_name:",cate_name)
    
    #뭐 관련 도서인지 메시지 전송. 
    print('{NAME} 관련 도서 추천해드릴게요.'.format(NAME=cate_name))
    msg = '{NAME} 관련 도서 추천해드릴게요😍'.format(NAME=cate_name)
    params = {'chat_id':chat_id, 'text': msg}
    response = requests.post(url, json=params)
    
    #해당 카테고리 도서 불러오기.
    interpark_API_KEY = "key=[interpark_API_KEY]"
    request = requests.get('http://book.interpark.com/api/bestSeller.api?'+interpark_API_KEY+'&categoryId='+code+'&output=json')
    genre_book = request.content.decode('utf-8')
    search_result = json.loads(genre_book)
    book_list = []
    #필요항목 추출
    for i in range(len(search_result['item'])):
        title = search_result['item'][i]['title']
        author = search_result['item'][i]['author']
        publisher = search_result['item'][i]['publisher']
        description = search_result['item'][i]['description']
        link = search_result['item'][i]['link']
    
        book_list.append('◇제목: <b>' + title +'</b> \r\n◇저자: <b>'+ author +'</b>     ◇출판사: <b>'+ publisher + '</b>\r\n◇내용: '+ description + '\r\n'+ link)
    
    #api에서 가져온 book_list의 데이터 랜덤으로 섞어준다.
    new_list = []
    new_list = random.shuffle(book_list)
    print("book_list개수:",new_list)
    #5개만 출력
    #book_list 갯수가 5보다 크면, 5개까지만 전송. 5보다 작거나 같으면, 모두 전송. 
    if len(book_list)>4:
        for index, book_info in enumerate(book_list):
            book_info = str(book_list[index])
            print("book_info:",index+1, book_info)
            if index >4:
                print('index:',index,'멈춤')
                break
            else:
                print('index:',index,'전송')
                params = {'chat_id':chat_id, 'text': book_info, 'parse_mode':'HTML'}
                response = requests.post(url, json=params) 
                print("response",response,"chat_id:",chat_id)            
    else:
         for index, book_info in enumerate(book_list):
             book_info = str(book_list[index])
             print("book_info:",index+1, book_info)
             params = {'chat_id':chat_id, 'text': book_info, 'parse_mode':'HTML'}
             response = requests.post(url, json=params) 
             print("response",response,"chat_id:",chat_id)
    
    #send_curate(chat_id, '도서추천')       
    genre_end(chat_id, '장르별 검색 결과')
    
    return 0

def genre_end(chat_id, text='장르별 검색 결과'):
    print("**********************************")
    print("[GENRE_END]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {                                        
            'keyboard':[[{'text':'다른 장르도서 검색하기'}],[{'text':'메뉴로 이동'}]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }   
    params = {'chat_id':chat_id, 'text': '다른 장르도서를 검색하시겠습니까?😊', 'reply_markup' : keyboard} #Markdown or HTML 
    response = requests.post(url, json=params)   
    return 0 
    
    
    
# '베스트셀러' 추천받는 기능: 
# 국내도서 or 외국 도서 선택하면 해당 도서의 베스트셀러10위까지가 메시지로 전송된다.
def bestseller(chat_id, text='베스트셀러 추천'):
    print("**********************************")
    print("[BESTSELLER]:",chat_id,text)
    print("**********************************")
    
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    keyboard = {                                        
            'keyboard':[[{'text':'국내도서'},{'text':'외국도서'}],[{
                    'text': '메뉴로 이동'
                        }]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }   
    params = {'chat_id':chat_id, 'text': '국내도서 or 외국도서를 선택해주세요.😎', 'reply_markup' : keyboard, 'parse_mode':'HTML'}
    response = requests.post(url, json=params)    
    
    return 0

# 현재: 베스트셀러 중 카테고리를 선택하면, 해당 카테고리의 베스트셀러리스트를 붙인다.
# (수정하기원하는 모양:  베스트셀러를 선택하면 국내or외국도서를 선택메뉴가 뜨고, 국내도서를 선택하면 국내도서 top10이 보인다. )
def bestsellerSearch(chat_id, category):
    print("**********************************")
    print("[CATEGORYSEARCH]:",chat_id, category)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    
    #메시지 내용(인문 or 경제경영 or 자기계발 or 취미/레저)에 따라 해당 categoryId를 부여한다. 
    if category == '국내도서':
        categoryId = '100'
    elif category == '외국도서':
        categoryId = '200'
    else:
        print("카테고리를 다시 선택해주세요.😎")
        #params = {'chat_id':chat_id, 'text': '카테고리를 다시 선택해주세요.😎'}
        #response = requests.post(url, json=params)
    
    #print("categoryId:",categoryId)
    interpark_API_KEY = "key=[interpark_API_KEY]"
    request = requests.get('http://book.interpark.com/api/bestSeller.api?'+interpark_API_KEY+'&categoryId='+categoryId+'&output=json')
    best = request.content.decode('utf-8')
    print("best type1:",type(best)) #str
    print("best내용:",best)
    search_result = json.loads(best)
    api_lists = []
    #필요항목 추출:제목,저자,출판사,링크
    for i in range(len(search_result['item'])):
        title = search_result['item'][i]['title']
        author = search_result['item'][i]['author']
        publisher = search_result['item'][i]['publisher']
        link = search_result['item'][i]['link']
    
        api_lists.append('제목: <b>' + title +'</b> | 저자: <b>'+ author +'</b> | 출판사: <b>'+ publisher+'</b>')
    # print('{NAME} 관련 베스트 셀러 목록입니다.'.format(NAME=category))
    text = '{NAME} 베스트 셀러 목록입니다.🙌'.format(NAME=category)
    params = {'chat_id':chat_id, 'text': text}
    response = requests.post(url, json=params)
    # print("api_lists:",api_lists)  
   
    
    #(인덱스+도서정보) x10개 메시지 전송.
    for index, api_list in enumerate(api_lists):
        api_list = api_lists[index]
        text = api_list
        no = str(index+1)+". "
        print("no:",no)
        #베스트셀러리스트 메시지 전송        
        params = {'chat_id':chat_id, 'text': no+text, 'parse_mode':'HTML'}
        response = requests.post(url, json=params)
        
        #9번까지만제한.
        if index==9:
            break
    
    bestseller(chat_id,'베스트셀러')
    
        
    return 0

# 감정별 추천: '오늘은 기분이 어떠신가요?라는 메시지가 전송됨과 동시에, 기쁨,슬픔,화남,즐거움 메뉴버튼이 나타난다.  
def emotion(chat_id, text='감정별 추천'):
    print("**********************************")
    print("[EMOTION]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{'text':'기쁨'},{'text': '슬픔'},{'text': '화남'},{'text':'즐거움'}]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }   
    
    params = {'chat_id':chat_id, 'text': '오늘은 기분이 어떠신가요?🧐', 'reply_markup' : keyboard}
    response = requests.post(url, json=params)  
      
    return 0


# 감정별 추천 - 도서추천해주기.
# 
def curate_book(chat_id, text):
    print("**********************************")
    print("[CURATE_BOOK]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    #검색결과 저장할 변수
    title_list = []
    image_list = []
    author_list = []
    publisher_list = []
    link_list = []
    desc_list = []
    title_list, image_list, author_list, publisher_list, link_list, desc_list = getSearchResult(text)
    print("title_list:",title_list)
    
    for i in range(5):
        title = title_list[i]
        author = author_list[i]
        image = image_list[i]
        publisher = publisher_list[i]
        link = link_list[i]
        description = desc_list[i]
        book_info = "이미지:{image}    도서명:{title}    작가명:{author}    출판사:{publisher}    설명:{description}    링크:{link}".format(image=image, title=title, author = author, publisher = publisher, description = description, link = link)
        print("book_info:",book_info)
        
        params = {'chat_id':chat_id, 'text': book_info, 'parse_mode':'HTML'}
        response = requests.post(url, json=params) 
    
    #back(chat_id, '뒤로')
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{'text':'다른 감정 선택'}],[{'text':'메뉴로 이동'}]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }   
    
    params = {'chat_id':chat_id, 'text': '도서추천 결과입니다.', 'reply_markup' : keyboard}
    response = requests.post(url, json=params)  

    return 0

# '화남'을 선택했을 때, 관련도서를 찾아주겠다는 문구. 
def emotion_answer(chat_id, text='찾아드릴게요.'):
    print("**********************************")
    print("[EMOTION_ANSWER]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    params = {'chat_id':chat_id, 'text':'화남을 선택하셨네요. 마음을 다스릴 수 있는 도서 추천해드릴게요😄' }
    response = requests.post(url, json=params)   
    
    return 0


def noservice(chat_id, text='서비스준비중'):
    print("**********************************")
    print("[NOSERVICE]:",chat_id,text)
    print("**********************************")
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   
    keyboard = {                                        
            'keyboard':[[{'text':'다른 감정 선택'}],[{'text':'메뉴로 이동'}]],
            'one_time_keyboard' : True,
            'resize_keyboard' : True
            }   
    params = {'chat_id':chat_id, 'text':'서비스 준비중입니다.😭', 'reply_markup':keyboard }
    response = requests.post(url, json=params)   
    
    return 0

# 받은 내용을 json에 저장한다.
def save():
    print("[SAVE]")
    if request.method == 'POST':
        # POST형식으로 데이터가 들어오면 json화 시켜서 message라는 변수에 할당
        message = request.get_json()
        
        # response.json 이라는 파일을 w (쓰기형식) 으로 열어주고
        # (With 문이 끝날때까지)
        # 내부 내용은 UTF-8 인코딩을 따른다 
        # 열어둔 파일은 f 라고 부른다 (as f) 
        with open('response.json', 'w', encoding='UTF-8') as f:
            
            # message라는 데이터를 f라는 파일에 들여쓰기 4칸
            # ASCII 값은 허용하지 않는다 
            json.dump(message, f, indent=4, ensure_ascii=False)
     
        # 성공적으로 진행되면 상태를 200으로 표시
        # https://developer.mozilla.org/ko/docs/Web/HTTP/Status
        return Response('ok', status=200)
    else:
        return "Hello World!"
    
# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        print(message)
                
        with open('response.json', 'w', encoding='UTF-8') as f:
            json.dump(message, f, indent=4, ensure_ascii=False)
        
        # 접속한 유저의 chat_id, msg를 불러오는 함수
        chat_id, last_name, msg = parse_message(message)
        
        # 접속 시작!
        if msg == '/start' or msg == '/시작':
            print("chatbot start!")
            # 접속한 유저에게 인사메시지를 보내는 함수
            send_hello(chat_id, last_name, '/start')
            
        #도서검색
        elif msg == '도서 검색':
            send_search(chat_id, '도서검색')       
        #s문자와 함께 도서명을 입력하여 도서를 검색한다.   
        elif msg[0]=='>':
            book = msg[1:]
            print('book:',book)
            search_book(chat_id, book)
        
        #도서추천(베스트셀러/장르별/기분별) 선택지 나타남
        elif msg == '도서 추천' or '도서추천' in msg:
            send_curate(chat_id, '도서 추천')
        
        #베스트셀러 추천
        elif msg == '베스트셀러':
            bestseller(chat_id, msg)
        elif msg in '국내도서' or msg in '외국도서':
            #베스트셀러 카테고리 메시지 전송    
           
            bestsellerSearch(chat_id, msg)
        #장르별 추천
        elif msg == '장르별' or '다른 장르도서' in msg:
            genre(chat_id,msg)
        #장르별 도서 검색 후 나타나는 메뉴버튼.
        elif '장르별 검색 결과' in msg:
            genre_end(chat_id, msg)
        
        elif 'code' in msg or 'Code' in msg:
            code = msg[4:]
            print("code??:",code)
            genreSearch(chat_id, code)
        
        #기분(기쁨,슬픔,화남,즐거움) 네가지 감정 선택지 나타남
        elif msg in '감정별' or msg == '다른 감정 선택': 
            emotion(chat_id, msg)
        #ex. 화남일 때 도서 추천.    
        elif msg == '화남':
            emotion_answer(chat_id, '화남')
            curate_book(chat_id, '마음')
        #ex. 서비스를 하고 있지 않음을 알림.
        elif '기쁨' in msg or '슬픔' in msg or '즐거움' in msg:
            noservice(chat_id, msg)
            
        #기타
        #메뉴버튼 띄우기    
        elif msg == '뒤로':
            back(chat_id, msg)
        
        #메뉴(도서검색,도서추천) 화면으로 이동    
        elif '메뉴' in msg:
            menu(chat_id, msg)
        
        else:
            menu(chat_id, msg)
        # 보낸 메시지 response.json에 저장.
        save()
        
        # 여기까지 오류가 없으면 서버상태 200 으로 반응
        return Response('ok', status=200)
    else:
        return 'Hello World!'

# Python 에서는 실행시킬때 __name__ 이라는 변수에
# __main__ 이라는 값이 할당
"""
if __name__ == '__main__':
    print("start")
    app.run(port = 5000)
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
