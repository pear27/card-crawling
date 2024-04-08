from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import re
import pandas as pd
from datetime import datetime
from io import BytesIO
from PIL import Image
import boto3
from selenium.webdriver.common.by import By
import configparser

config = configparser.ConfigParser()
config.read('/crawling/config.ini')

AWS_S3_ACCESSKEY = config['s3']['AWS_S3_ACCESSKEY']
AWS_S3_SECRETKEY = config['s3']['AWS_S3_SECRETKEY']
AWS_S3_BUCKET = config['s3']['AWS_S3_BUCKET']
AWS_S3_REGION = config['s3']['AWS_S3_REGION']

# S3연결
def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="{AWS_S3_ACCESSKEY}",
            aws_secret_access_key="{AWS_S3_SECRETKEY}",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 연결 성공")
        return s3

# 이미지 저장, 주소반환
def s3_put_object(cardImg,cardNo):
    try:
        data = urlopen(cardImg).read()
        img = Image.open(BytesIO(data))
        w, h = img.size
        if w < h : # 이미지가 세로인 경우
            img = img.rotate(90, expand=True)
            
            image_fileobj = BytesIO()
            img.save(image_fileobj, format='PNG')
            image_fileobj.seek(0)

            # S3에 업로드
            s3.upload_fileobj(image_fileobj, "{AWS_S3_BUCKET}", "lottecard/"+cardNo+".png",ExtraArgs={"ContentType": "image/jpg", "ACL": "public-read"})
            return "https://{AWS_S3_BUCKET}.s3.{AWS_S3_REGION}.amazonaws.com/lottecard/"+cardNo+".png"
        else:
            return cardImg
    except Exception as e:
        return False

# 페이지 크롤링 함수
def cardCrawling (cardurl):
    benefits=""
    
    cardhtml=urlopen(cardurl)
    cardbs=BeautifulSoup(cardhtml,'html.parser')
    
    # benefits
    benes = cardbs.findAll('div',{'class','bnfCont'})
    if len(benes) == 0:
        beneLists = cardbs.find('ul',{'class','toggleList'}).findAll('li',recursive=False)
        for beneList in beneLists:
            titlebene = beneList.find('a').text.replace('\t','').replace('\r','').replace('\n','').replace(' ','')
            if titlebene=="L.POINT" or titlebene=="가족카드" or titlebene== "가족카드안내" or titlebene== "연회비": continue
            benefits+="<"+titlebene+"> "
            details = beneList.find('div',{'class','toggleCont'}).findAll(recursive=False)
            for detail in details:
                if str(detail)[1:6]=="table": 
                    benefits+=str(detail).replace('\n','')
                elif str(detail)[1:3]=="h3": 
                    benefits+="["+detail.text+"]"
                elif str(detail)[1:3]=="h4": 
                    benefits+="/"+detail.text+": "
                elif str(detail)[1:6]=="style": 
                    continue
                else:
                    benefits+=detail.text.replace("\n","").replace('\r','').replace('\t','')
            benefits.replace('\n','').replace('\r','').replace('\t','')
            benefits+="\n"
    else:
        for bene in benes:
            titlebene=bene.find('h3').text
            if titlebene=="L.POINT" or titlebene=="가족카드" or titlebene== "가족카드 안내" or titlebene== "연회비" or titlebene== "혜택 모아보기": continue
            benefits+="<"+titlebene+">"
            sections = bene.findAll('div',{'class','toggle'})
            for section in sections:
                beneNames=section.find('h4')
                beneNameText=beneNames.text
                benefits+="["+beneNameText+"] "
                details = section.find('div',{'class','toggleCont'}).findAll(recursive=False)

                for detail in details:
                    if str(detail)[1:6]=="table": 
                        benefits+=str(detail).replace('\n','')
                    elif str(detail)[1:3]=="h3": 
                        benefits+="["+detail.text+"]"
                    elif str(detail)[1:3]=="h4": 
                        benefits+="/"+detail.text+": "
                    elif str(detail)[1:6]=="style": 
                        continue
                    else:
                        benefits+=detail.text.replace("\n","").replace('\r','').replace('\t','')
                benefits.replace('\n','').replace('\r','').replace('\t','')
            benefits+="\n"
            benefits=benefits.replace("'","")
            
    return benefits 

def cardList(associate):
    url = 'https://www.lottecard.co.kr/app/LPCDADA_V100.lc'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # 웹 페이지 로드
    driver.get(url)

    if(associate):
        # 제휴 카드 클릭
        link = driver.find_element(By.LINK_TEXT,"제휴")
        link.click()
        time.sleep(5)

    # Selenium으로 페이지 스크랩
    rendered_html = driver.page_source

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(rendered_html, 'html.parser')

    # 더보기 버튼 끝까지 누르기
    while True:
        new_render_html=driver.page_source
        soup = BeautifulSoup(new_render_html, 'html.parser')
        if soup.find('button',{'id':'btnMore'}) is None: break
        driver.find_element("id","btnMore").click()
        time.sleep(3)

    return soup.find('ul', {'id':'ajaxCardList'}).findAll('li')


name = []
img_url = []
benefits = []
created_at = []


for card in cardList(False):
    cardNo = card.find('a').get('onclick')
    cardNo = re.search(r"'(.*?)'", cardNo).group(1)
    
    cardurl='https://www.lottecard.co.kr/app/LPCDADB_V100.lc?vtCdKndC='+cardNo
    
    cardImg= "https:" + card.find('img').get('src')
    img_url.append("https://once-s3.s3.ap-northeast-2.amazonaws.com/lottecard/"+cardNo+".png")
    
    cardName=card.find('b').text
    name.append(cardName)

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ["+cardName+"] --- 웹 페이지에 접속 중... ")
    
    benefit = cardCrawling(cardurl)
    benefits.append(benefit)

    now_datetime = datetime.now()
    formatted_now = now_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    created_at.append(formatted_now)

for card in cardList(True):
    cardNo = card.find('a').get('onclick')
    cardNo = re.search(r"'(.*?)'", cardNo).group(1)
    
    cardurl='https://www.lottecard.co.kr/app/LPCDADB_V100.lc?vtCdKndC='+cardNo
    
    cardImg= "https:" + card.find('img').get('src')
    img_url.append("https://once-s3.s3.ap-northeast-2.amazonaws.com/lottecard/"+cardNo+".png")
    
    cardName=card.find('b').text
    name.append(cardName)

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ["+cardName+"](제휴) --- 웹 페이지에 접속 중... ")
    
    benefit = cardCrawling(cardurl)
    benefits.append(benefit)

    now_datetime = datetime.now()
    formatted_now = now_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    created_at.append(formatted_now)

    
card_company_id = [5] * len(name)
type = ["CreditCard"] * len(name)

data = {"card_company_id":card_company_id, "name" : name, "img_url" : img_url, "benefits": benefits, "created_at": created_at,"type":type}
df = pd.DataFrame(data)

df.to_csv("/crawling/Lotte/credit_benefit.csv", encoding = "utf-8-sig", index=False)
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" 롯데카드 신용카드 크롤링 완료", flush=True)