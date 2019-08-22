
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
import json

CLIENT_ID = '[NAVER_API_KEY]'
CLIENT_SECRET = 'OeVF11yjte'

request = Request('https://openapi.naver.com/v1/search/book?query='+quote('도끼 박웅현'))
request.add_header('X-Naver-Client-Id', CLIENT_ID)
request.add_header('X-Naver-Client-Secret', CLIENT_SECRET)
response = urlopen(request).read().decode('utf-8')
print("response!!!!!",response)


search_result = json.loads(response)


title_list = []
image_list = []
author_list = []
publisher_list = []
link_list = []
desc_list = []




"""



title = search_result['items'][0]['title'] #차례로,  items, index, 책제목
image = search_result['items'][0]['image']
author = search_result['items'][0]['author']
publisher = search_result['items'][0]['publisher']
link = search_result['items'][0]['link']
desc = search_result['items'][0]['description']

print("책 이름 : " + title)
print("이미지: " + image)
print("작가 : " + author)
print("출판사 : " + publisher)
print("링크 : " + link)
print("책 설명 : " + desc)

book_list = []
    
for i in range(len(search_result['items'])):
    book_list.append(search_result['items'][i])
    print(book_list)
    
    
 """   

    
    
#검색결과 딕셔너리.
def getSearchResult(keyword):
    try:
        request = Request('https://openapi.naver.com/v1/search/book?query='+quote(keyword))
        request.add_header('X-Naver-Client-Id', CLIENT_ID)
        request.add_header('X-Naver-Client-Secret', CLIENT_SECRET)      
        response = urlopen(request).read().decode('utf-8')    
      
        return response
    except:
        print('검색 결과가 없습니다.')
        
    search_result = json.loads(response)
    print('keyword:',search_result)
    
    book_list = []
    
    for i in range(len(search_result['items'])):
        book_list.append(search_result['items'][i])
        
        
    print(book_list)    
    return book_list
        

    
   
   
   
   
   
   
   
   
   
   
   
   
   
   