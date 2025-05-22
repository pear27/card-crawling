import json
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime


with open("config.json", "r") as f:
    config = json.load(f)

chrome_path = config.get("chrome_path")


# 이벤트 목록 크롤링 함수
def eventList():
    print("======= [삼성] 진행중인 이벤트 정보 리스트업 =======")

    event_codes = []
    event_images = []
    event_subjects = []
    event_start = []
    event_end = []

    options = webdriver.ChromeOptions()  # Chrome 드라이버 설정
    options.binary_location = chrome_path  # Chrome 설치된 경로로 변경
    options.add_argument("--headless")  # 브라우저 창 없이 실행 (필요시 제거)
    driver = webdriver.Chrome(service=Service(), options=options)

    # 페이지 열기
    url = "https://www.samsungcard.com/personal/event/ing/UHPPBE1401M0.jsp"
    driver.get(url)

    # li 요소가 로드될 때까지 대기
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "ul#board_append > li")
            )
        )

        # <li> 목록 수집
        event_items = driver.find_elements(By.CSS_SELECTOR, "ul#board_append > li")

        for item in event_items:
            # 이벤트 고유 코드 
            code = item.get_attribute("id")
            if code:
                event_codes.append(code)

            # 이미지 URL
            try:
                img_tag = item.find_element(By.CSS_SELECTOR, "img.m_display")
                img_src = img_tag.get_attribute("src")
            except:
                img_src = ""
            event_images.append(img_src)

            # 제목
            try:
                subject = item.find_element(By.CSS_SELECTOR, "p.tit").text.strip()
            except:
                subject = ""
            event_subjects.append(subject)

            # 날짜 → start_date / end_date
            start_date, end_date = "", ""
            try:
                date_text = item.find_element(By.CSS_SELECTOR, "span.date").text.strip()
                if "~" in date_text:
                    start_str, end_str = date_text.split("~")
                    start_date = datetime.strptime(start_str, "%Y.%m.%d").strftime("%Y-%m-%d")
                    end_date = datetime.strptime(end_str, "%Y.%m.%d").strftime("%Y-%m-%d")
            except:
                pass
            event_start.append(start_date)
            event_end.append(end_date)

    finally:
        driver.quit()


    # 결과 저장
    data = {
        "event_code": event_codes,
        "event_subject": event_subjects,
        "event_image": event_images,
        "event_start": event_start,
        "event_end": event_end,
    }
    df = pd.DataFrame(data)
    df.to_csv("./Samsung_event_list.csv", encoding="utf-8-sig")
    print("✅ 이벤트 정보를 Samsung_event_list.csv로 저장 완료.")
    

eventList()
