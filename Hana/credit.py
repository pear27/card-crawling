import pandas as pd
import time
from datetime import datetime
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

'''
    카드 정보 조회
    hana_creditCardInfos.csv : card_name, card_url, card_img
'''
url = "https://www.hanacard.co.kr/OPI31000000D.web?schID=pcd&mID=OPI31000005P&CT_ID=241704030444153#none"

chrome_options = Options()
chrome_options.add_argument('--headless')  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.implicitly_wait(20)
print("======= [하나] 신용 카드 정보 크롤링 =======")
print("웹 페이지에 접속 중...")
driver.get(url)
time.sleep(3)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

card_names = []
card_urls = []
card_imgs = []

tabs = driver.find_elements(By.CSS_SELECTOR, "#stc_list > li")
 
for tab in tabs:
    tab.click()
    
    time.sleep(3)
    tab_content = driver.page_source
    soup = BeautifulSoup(tab_content, 'html.parser')
    
    # 각 탭에서 카드 정보 추출 ==========
    main_area = soup.find('article', {'class': 'card_main_area'})
    card_ul = main_area.find('ul',{'class': 'card_slide_area'})
    card_li = card_ul.find_all('li', {'class': 'li'})
    
    for i in range(len(card_li)):
        # 카드 이름 
        name = card_li[i].find('dl',{'class': 'txt'}).find('dt').text
        card_names.append(name)
                
        # 카드 고유 번호
        url_btn = card_li[i].find('ul', {'class': 'btn'}).find_all('li')[1]
        a_tag = url_btn.find('a', {'class': 'btn_ty04'})

        onclick_value = a_tag.get('onclick')
        url = onclick_value.split("'")[1]
        card_urls.append(url)
        
        # 카드 이미지
        img = card_li[i].find('img')['src']
        card_imgs.append('https://www.hanacard.co.kr' + img)

print("작업을 완료했습니다.")
driver.quit()

data = {"card_name" : card_names, "card_url" : card_urls, "card_img": card_imgs}
df = pd.DataFrame(data)

df.to_csv("./hana_creditCardInfos.csv", encoding = "utf-8-sig")

'''
    전체 카드 혜택 크롤링
    credit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''
card_infos = pd.read_csv('./hana_creditCardInfos.csv')


card_urls = card_infos['card_url'].tolist()
name = card_infos['card_name'].tolist()
img_url = card_infos['card_img'].tolist()

card_company_id = [6] * len(card_urls) # 하나카드
benefits = []

created_at = []
type = ["CreditCard"] * len(card_urls)

print("======= [하나] 전체 카드 혜택 정보 크롤링 =======")
mID_urls = [str(url).zfill(5) for url in card_urls] # 다섯 자리로 맞추기

for i, url in enumerate(card_urls):
    url = f'https://www.hanacard.co.kr/OPI41000000D.web?schID=pcd&mID=PI410{mID_urls[i]}P&CD_PD_SEQ={url}&'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver.implicitly_wait(20)
    now = datetime.now()
    created_at.append(now)
    print(f"{now} [{card_names[i]}] --- 웹 페이지에 접속 중... ({i+1}/{len(card_urls)})")

    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    tab_list = soup.find_all('div', {'class': 'tab_cont'})
    benefit = ''

    if len(tab_list) == 0: # 탭이 하나도 없는 경우
        card_view_detail = soup.find('div', {'class': 'card_view_detail'})
        info_list = card_view_detail.find('ul', {'class': 'card_li'}).find_all('li', {'class': 'list'})
        
        for info in info_list:
            tit = info.find('dt', {'class': 'tit'})
            tit = str(tit.get_text(separator=' ', strip=True))
            benefit += f'[{tit}]'
                
            info_txt_list = info.find('dd', {'class': 'txt'}).find_all('li', {'class': 'blt1'})
            for txt in info_txt_list:
                info_txt = str(txt.get_text(separator=' ', strip=True))
                benefit += f'{info_txt} '
            
    elif len(tab_list) == 1:  
        title = tab_list[0].find('h5', {'class': 'blind'})
        if title:
            title = str(title.get_text(separator=' ', strip=True))
            benefit += f'###{title}'

        cont_list = tab_list[0].find_all('div', {'class': 'cont'})

        for cont in cont_list:
            cont_tit = cont.find('h6', {'class': 't_tit'})
            if cont_tit:
                cont_tit = str(cont_tit.get_text(separator=' ', strip=True))
                benefit += f'[{cont_tit}]'
                
            tables = cont.select('table')
            for table_num, table in enumerate(tables):

                # 표가 있을 때만 출력
                if table:
                    caption = table.find('caption').text
                    benefit += caption
                    rows = table.find_all('tr')
                    for j, row in enumerate(rows):
                        cells = row.find_all(['th', 'td'])
                        row_data = []

                        for cell in cells:
                            colspan = int(cell.get('colspan', 1))
                            content = cell.text.strip()
                            row_data.extend([content] * colspan)

                        row_string = ' '.join(['({})'.format(data) for data in row_data])
                            
                        # 각 행을 설명하는 문장 출력
                        sentence = f"표의 {j + 1}번째 행은 {row_string}로 이루어져 있습니다."
                        benefit += sentence
                            
            cont_ul = cont.find_all('ul', recursive=False)
            if cont_ul:
                for ul in cont_ul:
                    cont_li = ul.find_all('li', recursive=False)
                    for li in cont_li:
                        # li 태그 하위에 table이 없는 경우에만 처리
                        if not li.find('table'):
                           benefit += li.text    
    else:
        # 주요 혜택
        title = tab_list[0].find('h5', {'class': 'blind'}).text
        benefit += f'###{title}'
        
        info_list = tab_list[0].find('ul', {'class': 'card_info_list'}).find_all('li')

        for info in info_list:
            tit = info.find('div', {'class': 'tit'}).find('p')
            tit = str(tit.get_text(separator=' ', strip=True))
            benefit += f'[{tit}]'
                
            info_txt = info.find('div', {'class': 'inner'}).find('p')
            info_txt = str(info_txt.get_text(separator=' ', strip=True))
            benefit += info_txt
                     
        # 주요 혜택 제외 나머지 탭
        for tab in tab_list[1:]:
            title = tab.find('h5', {'class': 'blind'})
            if title:
                title = str(title.get_text(separator=' ', strip=True))
                benefit += f'###{title}'

            cont_list = tab.find_all('div', {'class': 'cont'})

            for cont in cont_list:
                cont_tit = cont.find('h6', {'class': 't_tit'})
                if cont_tit:
                    cont_tit = str(cont_tit.get_text(separator=' ', strip=True))
                    benefit += f'[{cont_tit}]'

                
                tables = cont.select('table')
                for table_num, table in enumerate(tables):
                    # 표가 있을 때만 출력
                    if table:
                        caption = table.find('caption').text
                        benefit += caption
                        rows = table.find_all('tr')
                        for j, row in enumerate(rows):
                            cells = row.find_all(['th', 'td'])
                            row_data = []

                            for cell in cells:
                                colspan = int(cell.get('colspan', 1))
                                content = cell.text.strip()
                                row_data.extend([content] * colspan)

                            row_string = ' '.join(['({})'.format(data) for data in row_data])
                            
                            # 각 행을 설명하는 문장 출력
                            sentence = f"표의 {j + 1}번째 행은 {row_string}로 이루어져 있습니다."
                            benefit += sentence
                            
                cont_ul = cont.find_all('ul', recursive=False)
                if cont_ul:
                    for ul in cont_ul:
                        cont_li = ul.find_all('li', recursive=False)
                        for li in cont_li:
                            # li 태그 하위에 table이 없는 경우에만 처리
                            if not li.find('table'):
                                benefit += li.text
                            
    benefits.append(benefit)

print("작업을 완료했습니다.")
driver.quit()

'''
    전체 카드 혜택 크롤링
    credit_benefit.csv : card_company_id, name, img_url, benefits, created_at, type
'''

data = {"card_company_id": card_company_id, "name": name, "img_url": img_url, "benefits" : benefits, "created_at": created_at, "type": type}
df = pd.DataFrame(data)

df.to_csv("./credit_benefit.csv", encoding = "utf-8-sig", index=False)