import sys

import csv
import pymysql
import datetime
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

db_host = config['database']['host']
db_user = config['database']['user']
db_password = config['database']['password']
db_database = config['database']['database']
db_charset = config['database']['charset']

# 데이터베이스 연결 설정
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_database,
    charset=db_charset,
    cursorclass=pymysql.cursors.DictCursor
)

current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

'''
    1. 국민 신용카드 데이터베이스 저장
        python3 ./Kookmin/DatabaseInsert.py Credit

    2. 국민 체크카드 데이터베이스 저장
        python3 ./Kookmin/DatabaseInsert.py Debit
'''
if sys.argv[1] == 'Credit':
    insert_type = '신용카드'
    csv_file = 'credit'
elif sys.argv[1] == 'Debit':
    insert_type = '체크카드'
    csv_file = 'debit'

try:
    with connection.cursor() as cursor:
        # CSV 파일 읽기
        with open(f'./Kookmin/{csv_file}_benefit.csv', 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            
            next(csvreader)
            
            for row in csvreader:
                card_company_id, name, img_url, benefits, created_at, type = row

                select_query = "SELECT * FROM card WHERE name = %s"
                cursor.execute(select_query, (name,))
                existing_card = cursor.fetchone()

                if existing_card: # 이미 존재하는 카드인 경우
                    update_query = """
                        UPDATE card
                        SET benefits = %s, updated_at = %s
                        WHERE name = %s
                    """
                    cursor.execute(update_query, (benefits, current_time, name))
                else: # 새로운 레코드 삽입
                    insert_query = """
                        INSERT INTO card
                        (card_company_id, name, img_url, benefits, created_at, type) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (card_company_id, name, img_url, benefits, created_at, type))
        
        connection.commit()
        print(f"{current_time} [국민 {insert_type}] --- DB update 완료 ")

finally:
    connection.close()
