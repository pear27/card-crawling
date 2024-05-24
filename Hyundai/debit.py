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
type = ["DebitCard"] * len(card_urls)

# 크롤링 정보 정리 (특수문자 제거 및 줄바꿈 제거)
def remove_blank(text):

    text_str = str(text)
    cleaned_text = ' '.join(text_str.split())

    return cleaned_text

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
        if title and (title.text.strip()[-2:] in ["적립"]):
            benefit += f'###{title.text.strip()}'
            benefit_container= popup_containers[i].find('div', class_='layer_body')
            benefit_title = benefit_container.find('div', class_='box_top_tit')
            benefit_body = benefit_title.find_next_sibling()
            benefit += f'[{benefit_title.text.strip()}]'
            benefit += benefit_body.text.strip()

        if title and (title.text.strip()[-2:] in ["사용", "제공"]):
            benefit += f'###{title.text.strip()}'
            benefit_container= popup_containers[i].find('div', class_='layer_body')
            benefit_title_list = benefit_container.find_all('div', class_='box_tit')
            for benefit_title in benefit_title_list:
                benefit += f'[{benefit_title.text.strip()}]'
                benefit_body = benefit_title.find_next_sibling()
                if benefit_body and not benefit_body.find('div', class_="accodWrap") and not benefit_body.find('div', class_="box_bg_gray"):
                    benefit += benefit_body.text.strip()
                elif benefit_body.find('div', class_="accodWrap"):
                    benefit_detail = benefit_body.find('div', class_="box_title02").text.strip()
                    benefit += benefit_detail
                else:
                    benefit_detail = benefit_body.find('div', class_="box_img_middle").text.strip()
                    benefit += benefit_detail

    benefits.append(remove_blank(benefit))

print("작업을 완료했습니다.")
driver.quit()

'''
    체크 카드 혜택 크롤링
    debit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''

data = {"card_company_id": card_company_id, "name": name, "img_url": img_url, "benefits" : benefits, "created_at": created_at, "type": type}
df = pd.DataFrame(data)

df.to_csv("./debit_benefit.csv", encoding = "utf-8-sig", index=False)