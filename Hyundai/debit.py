import pandas as pd
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

'''
    체크 카드 리스트 조회
    hyundai_checkcardInfos.csv : card_name, card_url, card_img
'''
url = "https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=C#aTab_2"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-web-security')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.implicitly_wait(20)
print("======= [현대] 신용 카드 리스트 크롤링 =======")
print("웹 페이지에 접속 중...")
driver.get(url)
time.sleep(3)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

card_names = []
card_urls = []
card_imgs = []

ul_class = soup.find_all('ul', class_='list05')
for i in range(len(ul_class)):
    li_class= ul_class[i].find_all('li')
    if li_class:
        for j in range(len(li_class)):
            name = li_class[j].find('span', class_='h4_b_lt')
            if name:
                card_names.append(name.text.strip())
                card_img_element = li_class[j].find('img').get('src')
                card_imgs.append(card_img_element)
                card_url_code = card_img_element[-9:-6]
                card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=C&cardWcd=' + card_url_code + '&eventCode=00000')

print("작업을 완료했습니다.")
driver.quit()

data = {"card_name" : card_names, "card_url" : card_urls, "card_img": card_imgs}
df = pd.DataFrame(data)

df.to_csv("./hyundai_checkcardInfos.csv", encoding = "utf-8-sig")

'''
    신용 카드 혜택 크롤링
    debit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''
card_infos = pd.read_csv('./hyundai_checkcardInfos.csv')

card_urls = card_infos['card_url'].tolist()
name = card_infos['card_name'].tolist()
img_url = card_infos['card_img'].tolist()

card_company_id = [2] * len(card_urls)
benefits = []

created_at = []
type = ["CreditCard"] * len(card_urls)

print("======= [현대] 전체 카드 혜택 정보 크롤링 =======")
for i in range(len(card_urls)):

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-web-security')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.implicitly_wait(20)
    now = datetime.now()
    created_at.append(now)
    print(f"{now} [{card_names[i]}] --- 웹 페이지에 접속 중... ({i+1}/{len(card_urls)})")

    driver.get(card_urls[i])
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 상세 혜택 =============================================
    popup_containers = soup.find_all('div', class_='modal_pop')

    benefit_title = []
    benefit = ''

    for i in range(len(popup_containers)):
        title = popup_containers[i].find('div', class_='layer_head')
        if title and (title.text.strip()[-2:] == "적립" or title.text.strip()[-2:] == "사용"
                      or title.text.strip()[-2:] == "할인" or title.text.strip()[-5:] == "업그레이드"
                      or title.text.strip()[-3:] == "보너스" or title.text.strip()[-3:] == "서비스"
                      or title.text.strip()[-3:] == "트래블" or title.text.strip()[-3:] == "리워드"):
            benefit += f'###{title.text.strip()}'
            item_list = popup_containers[i].find('div', class_='layer_body')
            benefit += item_list.text.strip()

    benefits.append(benefit)

print("작업을 완료했습니다.")
driver.quit()

'''
    체크 카드 혜택 크롤링
    debit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''

data = {"card_company_id": card_company_id, "name": name, "img_url": img_url, "benefits" : benefits, "created_at": created_at, "type": type}
df = pd.DataFrame(data)

df.to_csv("./debit_benefit.csv", encoding = "utf-8-sig", index=False)



