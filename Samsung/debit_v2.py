import pandas as pd
import time
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

'''
    체크 카드 리스트 조회
    samsung_checkcardInfos.csv : card_name, card_url, card_img
'''
card_list_url = "https://www.samsungcard.com/home/card/cardinfo/PGHPPCCCardCardinfoCheckcard001"
html = urlopen(card_list_url)
soup = BeautifulSoup(html, 'html.parser')

print("======= [삼성] 체크 카드 리스트 크롤링 =======")
print("웹 페이지에 접속 중...")


card_names = []
card_urls = []
card_imgs = []

ul_tag = soup.find('ul', class_='lists')
list_elements = ul_tag.find_all('li')

for idx, element in enumerate(list_elements, 1):
    card_name_element = element.find('div', class_='tit-h4')
    card_names.append(card_name_element.text.strip())

    card_img_element = element.find_all('img')[1].get('src')
    card_imgs.append(card_img_element)

    card_url_code = card_img_element[-8:-4]
    card_urls.append('https://www.samsungcard.com/home/card/cardinfo/PGHPPCCCardCardinfoDetails001?code=ABP' + card_url_code)

print("작업을 완료했습니다.")

data = {"card_name" : card_names, "card_url" : card_urls, "card_img": card_imgs}
df = pd.DataFrame(data)

df.to_csv("./samsung_checkcardInfos.csv", encoding = "utf-8-sig")

'''
    체크 카드 혜택 크롤링
    debit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''
card_infos = pd.read_csv('./samsung_checkcardInfos.csv')

card_urls = card_infos['card_url'].tolist()
name = card_infos['card_name'].tolist()
img_url = card_infos['card_img'].tolist()

card_company_id = [3] * len(card_urls)
benefits = []

created_at = []
type = ["DebitCard"] * len(card_urls)

print("======= [삼성] 전체 카드 혜택 정보 크롤링 =======")
for i in range(len(card_urls)):
    now = datetime.now()
    created_at.append(now)
    print(f"{now} [{card_names[i]}] --- 웹 페이지에 접속 중... ({i+1}/{len(card_urls)})")

    html = urlopen(card_urls[i])
    soup = BeautifulSoup(html, 'html.parser')

    # 상세 혜택 =============================================
    tab_container = soup.find('section', class_='tab-container')
    tab_list = tab_container.find_all('div', class_='tab-section')
    benefit_title = []
    benefit = ''

    for i in range(1, len(tab_list)):
        benefit_title.append(tab_list[i].find('div', class_='dot-title').text.strip())
    
    for i in range(1, len(tab_list)):
        benefit += f'\n<{benefit_title[i-1]}>'
        benefit_list = tab_list[i].find_all('h5', class_='tit04')

        for title in benefit_list:
            if (title.text.strip() == "유의사항") or (title.text.strip() == "문의"):
                break
            benefit += f'[{title.text.strip()}]'
            next_sibling = title.find_next_sibling()
            if next_sibling.name == 'div' and 'table_col' in next_sibling.get('class', []):
                table = next_sibling.select_one('table')
                if table:
                    benefit += str (table).replace('\n','').replace('\r','').replace('\t','')
            elif next_sibling.name == 'ul':
                benefit += next_sibling.text.strip().replace('\n','').replace('\r','')
    benefits.append(benefit)

print("작업을 완료했습니다.")

'''
    체크 카드 혜택 크롤링
    debit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''

data = {"card_company_id": card_company_id, "name": name, "img_url": img_url, "benefits" : benefits, "created_at": created_at, "type": type}
df = pd.DataFrame(data)

df.to_csv("./debit_benefit.csv", encoding = "utf-8-sig", index=False)



