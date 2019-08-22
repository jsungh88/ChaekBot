import requests

import json

from urllib.request import urlopen


request = requests.get('http://book.interpark.com/api/bestSeller.api?key=[DaumAPI_KEY]&categoryId=100&output=json')
bast = request.text
search_result = json.loads(bast)

#반복문으로 타이틀 제목만 뺴오기.
api_list = []
for i in range(len(search_result['item'])):
    api_list.append(search_result['item'][i]['title'])

print(api_list)# -*- coding: utf-8 -*-

api_list = []
    for i in range(len(search_result['item'])):
        api_list.append(search_result['item'][i]['imageUrl'])
        api_list.append(search_result['item'][i]['title'])
        api_list.append(search_result['item'][i]['author'])
        api_list.append(search_result['item'][i]['publisher'])
        api_list.append(search_result['item'][i]['description'])
        api_list.append(search_result['item'][i]['url'])

    print("api_list:",api_list)
    
    api_list2.append(search_result['searchCategoryId'][i]
    api_list2.append(search_result['searchCategoryName'][i])
    print("api_list:",api_list2)
    
    
    