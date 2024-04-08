import pandas as pd
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

'''
    신용 카드 리스트 조회
    samsung_creditcardInfos.csv : card_name, card_url, card_img
'''
card_list_url = "https://www.samsungcard.com/home/card/cardinfo/PGHPPDCCardCardinfoRecommendPC001"
html = urlopen(card_list_url)
soup = BeautifulSoup(html, 'html.parser')


card_names = []
card_urls = []
card_imgs = []

card_tab_section = soup.find_all('div', class_='tab-section')

for i in range(2, len(card_tab_section)):
    ul_tag = card_tab_section[i].find('ul', class_='lists')
    list_elements = ul_tag.find_all('li')

    for idx, element in enumerate(list_elements, 1):
        card_name_element = element.find('div', class_='tit-h4')
        card_names.append(card_name_element.text.strip())

        card_img_element = element.find('img').get('src')
        card_imgs.append(card_img_element)

        card_url_code = card_img_element[-11:-4]
        card_urls.append('https://www.samsungcard.com/home/card/cardinfo/PGHPPCCCardCardinfoDetails001?code=' + card_url_code)

print("작업을 완료했습니다.")

# 중복 제거
unique_card_urls = list(set(card_urls))

data = {"card_name": [], "card_url": [], "card_img": []}

# 중복 제거된 card_url에 해당하는 정보만 데이터에 추가
for url in unique_card_urls:
    index = card_urls.index(url)
    data["card_name"].append(card_names[index])
    data["card_url"].append(card_urls[index])
    data["card_img"].append(card_imgs[index])

df = pd.DataFrame(data)

df.to_csv("./samsung_creditcardInfos.csv", encoding = "utf-8-sig")

'''
    신용 카드 혜택 크롤링
    credit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''
card_infos = pd.read_csv('./samsung_creditcardInfos.csv')

card_urls = card_infos['card_url'].tolist()
name = card_infos['card_name'].tolist()
img_url = card_infos['card_img'].tolist()

card_company_id = [3] * len(card_urls)
benefits = []

created_at = []
type = ["CreditCard"] * len(card_urls)

print("======= [삼성] 전체 카드 혜택 정보 크롤링 =======")
for i in range(len(card_urls)):

    
    now = datetime.now()
    created_at.append(now)
    print(f"{now} [{card_names[i]}] --- 웹 페이지에 접속 중... ({i+1}/{len(card_urls)})")

    html = urlopen(card_urls[i])
    soup = BeautifulSoup(html, 'html.parser')

    # 상세 혜택 =============================================
    tab_container = soup.find('section', class_='tab-container')
    tab_list = tab_container.find_all('div', role='tabpanel')

    benefit_title = []
    benefit = ''

    for i in range(len(tab_list)):
        tab_name = tab_list[i].find('div', class_='dot-title').text.strip()
        if tab_name not in ["요약", "카드이용TIP", "카드 디자인 소개", "네이버 디지털콘텐츠 적립 혜택 적용방법", "신세계포인트 적립 서비스", "세무지원 서비스", "BIZ SERVICE", "SPECIAL PLATE", "신세계백화점 제휴 서비스"]:
            benefit_title.append(tab_name)
    j = 0
    for i in range(len(tab_list)):
        tab_name = tab_list[i].find('div', class_='dot-title').text.strip()
        if tab_name in ["요약", "카드이용TIP", "카드 디자인 소개", "네이버 디지털콘텐츠 적립 혜택 적용방법", "신세계포인트 적립 서비스", "세무지원 서비스", "BIZ SERVICE", "SPECIAL PLATE", "신세계백화점 제휴 서비스"]:
            continue

        
        benefit += f'\n<{benefit_title[j]}>'
        j += 1

        benefit_list = tab_list[i].find_all('h5', class_='tit04')

        for title in benefit_list:
            if (title.text.strip() == "유의사항") or (title.text.strip() == "국제 브랜드사 서비스 공통 유의사항"):
                break

            benefit += f'[{title.text.strip()}]'
            next_sibling = title.find_next_sibling()
            if next_sibling is not None and next_sibling.name == 'div' and 'table_col' in next_sibling.get('class', []):
                table = next_sibling.select_one('table')
                if table:
                    benefit += str (table).replace('\n','').replace('\r','').replace('\t','')

            elif next_sibling is not None and next_sibling.name == 'ul':
                benefit += next_sibling.text.strip().replace('\n','')

    benefits.append(benefit)

print("작업을 완료했습니다.")

'''
    신용 카드 혜택 크롤링
    credit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''

data = {"card_company_id": card_company_id, "name": name, "img_url": img_url, "benefits" : benefits, "created_at": created_at, "type": type}
df = pd.DataFrame(data)

df.to_csv("./credit_benefit.csv", encoding = "utf-8-sig", index=False)



