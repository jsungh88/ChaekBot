# -*- coding: utf-8 -*-


# 챗봇ID : Chaeck_bot


# 텔레그램챗봇 method:  https://core.telegram.org/bots/api#available-methods

API_KEY = 'API_KEY'
user_id = 'userId'
URL = 'URL'


# Making requests 

# 1. API_KEY 에 해당되는 bot의 정보를 표시
# https://api.telegram.org/bot[API_KEY]/getMe

# 2. API_KEY 에 해당되는 bot의 업데이트 내역을 표시 
# https://api.telegram.org/bot[API_KEY]/getUpdates

# 3. API_KEY 에 해당되는 bot이 chat_id 인 사람에게 text를 보내도록함
# https://api.telegram.org/bot[API_KEY]/sendMessage?chat_id=[userId]&text=책봇안녕

# 4. SetWebhook
# https://api.telegram.org/bot[API_KEY]/setWebhook?url=[HostingAddress]

# 5. 할당받은 웹훅주소를 지우기
# https://api.telegram.org/bot[API_KEY]/deleteWebhook


#6. 웹훅정보 가져오기
# https://api.telegram.org/bot[API_KEY]/getWebhookInfo



# 포트포워딩 방법2
# ngrok 다운로드
# ngrok http 5000 --region ap
