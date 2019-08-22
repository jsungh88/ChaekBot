# -*- coding: utf-8 -*-

import requests
import json

from urllib.request import urlopen
#이인터파크 api 키
Interpark_API_KEY = "key=[Interpark_API_KEY]"
#카테고리번호
categoryId = '100'
#print(search_result)



#카테고리를 선택한다.
#인문 - 119, 자연과학 - 116, 경제경영 - 117, 자기계발 - 118, 취미/레저 - 124
#


#categoryID를 입력하면 해당카테고리 베스트셀러리스트를 보여준다.

def CategorySearch(category):
    if category == '인문':
        categoryId = '119'
    elif category == '자연과학':
        categoryId = '116'
    elif category == '경제경영':
        categoryId = '117'
    elif category == '자기계발':
        categoryId = '118'
    elif category == '취미/레저':
        categoryId = '124'
    else:
        print("카테고리명을 다시 입력해주세요.")
        
    #리스트 만들어주고 가져온 정보에서 타이틀만 넣어주기.
    request = requests.get('http://book.interpark.com/api/bestSeller.api?'+Interpark_API_KEY+'&categoryId='+categoryId+'&output=json')
    #best = request.encoding
    #print("Best:", request.encoding)
    #best = request.content
    
    #best = request.text
    #print("best:",best, "type:",type(best))
    #best.decode('utf-8','ignore')
    
    #best = request.text
    #print("type:",type(best))
    #best.encode("utf-8")
    #print("best:",best)
    best = request.content.decode('utf-8')
    search_result = json.loads(best)

    api_lists = []
    #필요항목 추출
    for i in range(len(search_result['item'])):
        title = search_result['item'][i]['title']
        author = search_result['item'][i]['author']
        publisher = search_result['item'][i]['publisher']
        link = search_result['item'][i]['link']
        api_lists.append('제목: ' + title +' 저자: '+ author +' 출판사: '+ publisher + link)
    print("api_lists:",api_lists)

    #목록코드에 따른 항목변화.
    if categoryId == '119':
        category = '인문'
    elif categoryId == '116':
        category = '자연과학'
    elif categoryId == '117':
        category = '경제경영'
    elif categoryId == '118':
        category = '자기계발'
    elif categoryId == '124':
        category = '취미/레저'
    print('{NAME} 관련 베스트 셀러 목록입니다.'.format(NAME=category))
    #리스트 전부 가져오지만
    for index, api_list in enumerate(api_lists):
        api_list = api_lists[index]
        text = api_list
        no = str(index+1)+". "
        print("no:",no)
       
        #9번까지만제한.
        if index==9:
            break

def search(chat_id, code):
    #해당 카테고리 도서 불러오기.
    interpark_API_KEY = "key=[Interpark_API_KEY]"
    request = requests.get('http://book.interpark.com/api/bestSeller.api?'+interpark_API_KEY+'&categoryId='+code+'&output=json')
    genre = request.content.decode('utf-8')
    search_result = json.loads(genre)
    book_list = []
    #필요항목 추출
    for i in range(len(search_result['item'])):
        title = search_result['item'][i]['title']
        author = search_result['item'][i]['author']
        publisher = search_result['item'][i]['publisher']
        #description = search_result['item'][i]['description']
        link = search_result['item'][i]['link']
    
        book_list.append('<제목: <b>' + title +'</b> \r\n저자: '+ author +' 출판사: '+ publisher + ' 링크: '+ link)
    
    #api에서 가져온 book_list의 데이터 랜덤으로 섞어준다.
    random.shuffle(book_list)
    
    #5개만 출력
    for index, book_info in enumerate(book_list):
        book_info = str(book_list[index])
        print("book_info:",index+1, book_info)
        params = {'chat_id':chat_id, 'text': book_info, 'parse_mode':'HTML'}
        response = requests.post(url, json=params) 
        print("response",response)
        #5번까지만제한.
        if index==4:
            break
        
        
#번호 스트링 타입으로 넣어주기
#인문
#CategorySearch('인문')

search('954489427','119')
