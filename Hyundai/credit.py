import pandas as pd
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

'''
    신용 카드 리스트 조회
    hyundai_creditcardInfos.csv : card_name, card_url, card_img
'''
url = "https://www.hyundaicard.com/cpc/ma/CPCMA0101_01.hc?cardflag=ALL"

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

card_section = soup.find_all('ul', class_='list05')

for i in range(len(card_section)):
    list_elements = card_section[i].find_all('div', class_='card_plt')

    for element in list_elements:
        card_name_element = element.find('span', class_='h4_b_lt')
        card_name = card_name_element.text.strip()

        if card_name == "기아":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=K#aTab_1'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-12:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=K&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "현대자동차":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=H'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-11:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=H&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "대한항공":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=D'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-11:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=D&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "American Express":
            url = 'https://www.hyundaicard.com/cpc/ma/CPCMA0101_01.hc?cardflag=AX'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-10:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardWcd=' + card_url_code)
            continue

        if card_name == "이마트":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=E'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-11:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=E&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "지마켓(스마일카드)":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=S'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-11:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=S&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "코스트코":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=T'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-12:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=T&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "미래에셋증권":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=MA'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-14:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "넥슨":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=N'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-11:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "KT":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=J&ctgrCd=050401'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-11:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "SKT":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=J&ctgrCd=050403'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-14:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "롯데면세점":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=J&ctgrCd=050605'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-12:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "SC제일은행":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=J&ctgrCd=050703'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-12:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "경차":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=J&ctgrCd=050802'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-11:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name == "화물차":
            url = 'https://www.hyundaicard.com/cpc/cr/CPCCR0621_11.hc?cardflag=J&ctgrCd=050803'
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            soup_deep1 = BeautifulSoup(html, 'html.parser')
            ul_class = soup_deep1.find_all('ul', class_='list05')
            for i in range(len(ul_class)):
                li_class= ul_class[i].find_all('li')
                if li_class:
                    for j in range(len(li_class)):
                        name = li_class[j].find('span', class_='h4_b_lt')
                        if name:
                            card_names.append(name.text.strip())
                            card_img_element = element.find('img').get('src')
                            card_imgs.append(card_img_element)
                            card_url_code = card_img_element[-10:-6]
                            card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardflag=MA&cardWcd=' + card_url_code + '&eventCode=00000')
            continue

        if card_name in ["쏘카", "제네시스", "야놀자ㆍ인터파크(NOL 카드)", "무신사", "SSG.COM", "네이버", "배달의민족", "스타벅스", "GS칼텍스", "LG U+", "기타", "현대홈쇼핑", "예스24", "하이마트", "The CJ", "coway-현대카드M Edition3", "LG전자-현대카드M Edition3", "햇살론", "인플카 현대카드"]:
            card_names.append(card_name_element.text.strip())

            card_img_element = element.find('img').get('src')
            card_imgs.append(card_img_element)

            card_url_a = element.find('a')
            card_url = card_url_a.get('href')
            print('코드' + card_url)
            card_urls.append('https://www.hyundaicard.com' + card_url)
            continue


        if card_name == "체크카드" or card_name == "Gift카드" or card_name == "후불하이패스카드":
            continue

        card_names.append(card_name_element.text.strip())

        card_img_element = element.find('img').get('src')
        card_imgs.append(card_img_element)

        card_code_a = element.find('a')
        card_code = card_code_a.get('onclick')
        if card_code:
            start_index = card_code.find("'") + 1
            end_index = card_code.find("'", start_index)
            card_url_code = card_code[start_index:end_index]

        if card_name in ["MY BUSINESS M Food&Drink", "MY BUSINESS M Retail&Service", "MY BUSINESS M Online Seller", "MY BUSINESS X Food&Drink", "MY BUSINESS X Retail&Service", "MY BUSINESS X Online Seller", "MY BUSINESS ZERO Food&Drink", "MY BUSINESS ZERO Retail&Service", "MY BUSINESS ZERO Online Seller"]:
            card_code2 = card_code_a.get('href')
            start_index = card_code2.find("'") + 1
            end_index = card_code2.find("'", start_index)
            card_url_code = card_code2[start_index:end_index]

        card_urls.append('https://www.hyundaicard.com/cpc/cr/CPCCR0201_01.hc?cardWcd=' + card_url_code)

print("작업을 완료했습니다.")
driver.quit()

data = {"card_name" : card_names, "card_url" : card_urls, "card_img": card_imgs}
df = pd.DataFrame(data)

df.to_csv("./hyundai_creditcardInfos.csv", encoding = "utf-8-sig")


'''
    신용 카드 혜택 크롤링
    credit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''
card_infos = pd.read_csv('./hyundai_creditcardInfos.csv')

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
                      or title.text.strip()[-3:] == "트래블" or title.text.strip()[-3:] == "리워드"
                      or title.text.strip()[-2:] == "절감"  or title.text.strip()[-2:] == "지원"):
            benefit += f'###{title.text.strip()}'
            item_list = popup_containers[i].find('div', class_='layer_body')
            benefit += item_list.text.strip()

    benefits.append(benefit)

print("작업을 완료했습니다.")
driver.quit()

'''
    신용 카드 혜택 크롤링
    credit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''

data = {"card_company_id": card_company_id, "name": name, "img_url": img_url, "benefits" : benefits, "created_at": created_at, "type": type}
df = pd.DataFrame(data)

df.to_csv("./credit_benefit.csv", encoding = "utf-8-sig", index=False)



