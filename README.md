# ChaekBot

## 프로젝트 소개
 사용자가 원하는 도서정보를 쉽고, 친숙하게 검색 및 추천할 수 있는 ‘텔레그램 책봇(Chaeck_bot)’입니다. Python과 web crawling, 공공데이터 API 사용법을 익히고, 이틀 간 진행하여 만든 프로젝트입니다. RestAPI를 사용하여 데이터를 가져왔고, 데이터포워딩은 Heroku를 사용하여 배포하였습니다. 
 
## 사용 기술
* Language : Python
* OS: Windows
* Web Server : Flask
* Server Hosting : Heroku
* Library : openpyxl, selenium, telegram API, NaverAPI, InterparkAPI

## 구현 기능
1. Telegram 챗봇 api 사용하여 챗봇 생성하기
2. NaverAPI, InterParkAPI 사용하여 도서정보 가져오기
3. Selenium라이브러리 사용 및 크롤링하여, 네이버 베스트 셀러 리스트 정보 사용하기
4. 엑셀 시트 데이터 불러와서 dictionary화 시켜 사용하기 (장르별 도서추천에 카테고리code정보 불러오기)
