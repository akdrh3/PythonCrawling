import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



#url of the website to be scraped
url = "https://www.wheretoshoot.org/"
wait_time=5 
delay_time=0.1

# # define the headers
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# req = requests.get(url, headers = headers)
# soup = BeautifulSoup(req.text, 'html.parser')
# p = soup.find_all(class_='checkbox')
# print(p)


# 크롬 드라이버로 해당 url에 접속
driver = webdriver.Chrome(ChromeDriverManager().install())

# (크롬)드라이버가 요소를 찾는데에 최대 wait_time 초까지 기다림 (함수 사용 시 설정 가능하며 기본값은 5초)
driver.implicitly_wait(wait_time)


# define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 인자로 입력받은 url 주소를 가져와서 접속
driver.get(url)
