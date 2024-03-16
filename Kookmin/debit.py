import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime

name = []
img_url = []
benefits = []
created_at = []

def findtableortext(str): # 테이블 추출
    try:
        thead = str.find('thead').findAll('th')
        sentence = " 표의 칼럼은 "

        for columnname in thead:
            columnname=columnname.text
            sentence+=columnname.replace('\n','')+", "
        sentence=sentence[0:-2]
        sentence += " 로 이루어져 있습니다."
        j=1
        tbodies = str.find('tbody').findAll('tr')

        for tbody in tbodies:

            tds = tbody.findAll('td')
            sentence += f"표의 {j}번째 행은 "
            
            for td in tds:
                sentence+=td.text.replace(",","").replace('\n','')+", "
            sentence=sentence[0:-2]
            sentence += " 로 이루어져 있습니다."
            j+=1
        
        return sentence
    except:
        sentence=str.text.replace('\n', '')
    return sentence

def findBenefitminititle(str): # 소제목 찾기
    sentence=""
    benetitle=""
    benecontent=""
    benetitle=str.find('div',{'class','tit'})
    for child in str.find_all(recursive=False):
        if benetitle is None:continue
        title=str.find('div',{'class','tit'}).text
        text=child.text
        if text == title: continue
        benecontent+=text
    if benetitle is not None: sentence+="["+benetitle.text.replace('\n', '')+"] "
    if benecontent is not None: sentence+=benecontent.replace('\n', '')

    return sentence

def findBenefit(detail): # 카드 혜택 크롤링
    benefitsentence=""
    content=detail.h2.text[7:]
    if content!="":
        if content.replace(' ','')=="서비스요약" or content.replace(' ','')=="서비스한눈에보기": return ""
        benefitsentence+="\n<"+content+"> "
    for child in detail.find_all(recursive=False):
        if str(child)[1:3]=="h2": 
            continue
        if str(child)[1:6]=="style": 
            continue
        if str(child)[:17] == '<div id="tabCon01':
            for d in child.findAll(recursive=False):
                if str(d)[1:3]=="h2": 
                    continue    
                if str(d)[1:6]=="style": 
                    continue    
                if str(d)[1:28]=='div class="benefitBox1 marT': 

                    for c in d.find_all(recursive=False):
                        # print(c)
                        if str(c)[:19]== '<div class="titArea':
                            benefitsentence+=findBenefitminititle(c)
                        if str(c)[1:6]=="style": 
                            continue  
                        else:
                            benefitsentence+=findtableortext(c)   
                else:
                    benefitsentence+=findtableortext(child)   
              
        else:
            if str(child)[:28] == '<div class="benefitBox1 marT':
                for c in child.find_all(recursive=False):
                    if str(c)[:19]== '<div class="titArea':
                        benefitsentence+=findBenefitminititle(c)
                    if str(c)[1:6]=="style": 
                        continue
                    else:
                        benefitsentence+=findtableortext(c)    
            else: benefitsentence+=findtableortext(child)
    return benefitsentence

def cate_page(url,cateIdx):
    html=urlopen(url+cateIdx)
    bs=BeautifulSoup(html,'html.parser')
    links = bs.findAll('div', {'class':'card-box__before'})
    for link in links:
        onclick_value=link.a.get('onclick')
        numbers=onclick_value[21:26]
        
        card_html=urlopen('https://card.kbcard.com/CRD/DVIEW/HCAMCXPRICAC0076?mainCC=a&cooperationcode='+numbers)
        card_bs=BeautifulSoup(card_html,'html.parser')
        cardName=card_bs.find('h1',{'class','tit'}).text

        if cardName not in name:
            name.append(cardName)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ["+cardName+"] --- 웹 페이지에 접속 중... ")
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ["+cardName+"] --- 이미 존재하는 카드입니다 ")
            continue

        img=card_bs.find('div',{'class','cardBoxInner'}).img.get('src')
        img_url.append(img)

        benefit=""

        w=card_bs.find('li',{'id':'topTab1'}).text.replace('\n','').replace(' ','').replace('\t','')
        if(w=="상세혜택"): tab='tabCon01'  # 주요혜택 있을 때 상세혜택 id
        else: tab='tabCon02'             # 주요혜택 없을 때 상세혜택 id

        summary=card_bs.find('div',{'class':'tabMulti marT20 multiLine2'}) # 상세혜택 안에 표

        if summary is None:                       # 표가 없는 경우
            if card_bs.find('div',{'id':'tabCon011'}): # 표 없지만 tabCon011, tabCon012 .. 에 저장되는 경우
                contents=card_bs.find('div',{'id':tab})
                details=contents.findAll('div', id=re.compile(f'^{re.escape(tab)}'),recursive=False)
                for detail in details:
                    benefit+=findBenefit(detail).replace('\t','')
            else:
                content=card_bs.find('div',{'id':tab}).div
                benefit+=findBenefit(content).replace('\t','')


        else:
            contents=card_bs.find('div',{'id':tab})
            details=contents.findAll('div', id=re.compile(f'^{re.escape(tab)}'),recursive=False)
            for detail in details:
                benefit+=findBenefit(detail).replace('\t','')

        benefit=benefit.replace('\'','').replace('\t','')
        benefits.append(benefit)
        
        now_datetime = datetime.now()
        formatted_now = now_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")   
        created_at.append(formatted_now)

    
url = 'https://card.kbcard.com/CRD/DVIEW/HCAMCXPRICAC0047?pageNo=1&cateIdx='
for i in range (1, 12):
    cateIdx = str(i)
    cate_page(url,cateIdx)

card_company_id = [1] * len(name)
type = ["DebitCard"] * len(name)

data = {"card_company_id":card_company_id, "name" : name, "img_url" : img_url, "benefits": benefits, "created_at": created_at,"type":type}
df = pd.DataFrame(data)
 
df.to_csv("debit_benefit.csv", encoding = "utf-8-sig", index=False)
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" 국민카드 체크카드 크롤링 완료")