from selenium import webdriver
from selenium.webdriver.common.by import By
import loader
from bs4 import BeautifulSoup

xpath = {'number': 'td:nth-child(1)', 'title': 'td:nth-child(2) > div:nth-child(1) > a', 'date': 'td:nth-child(4)', 'personnel': 'td:nth-child(5)', 'lecturer': 'td:nth-child(7)'}

# selenium driver 생성
def create_driver():
    driver = webdriver.Chrome('./chromedriver')
    driver.get(loader.get_env('login_url'))
    driver.implicitly_wait(10)
    return driver


# 로그인 후 크롤링 url 진입
def login(driver: webdriver.Chrome):
    email = loader.get_env('email')
    password = loader.get_env('password')

    driver.find_element(By.ID, 'username').send_keys(email)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'btn5.btn_blue2').click()

    driver.get(loader.get_env('crawling_url'))


# 크롤링 시작
def start(driver: webdriver.Chrome):
    driver.refresh()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    source = soup.select('#listFrm > table > tbody > tr')[1]
    
    result = {}
    for key in xpath.keys():
        result[key] = source.select_one(xpath[key]).get_text(strip=True).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ')

    return result
