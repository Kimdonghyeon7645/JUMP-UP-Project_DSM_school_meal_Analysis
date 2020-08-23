#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


menu = dict()
for i in range(1, 8):
    html = requests.get(f'http://dsmhs.djsch.kr/boardCnts/list.do?type=default&page={i}&m=020503&s=dsmhs&boardID=54797')
    soup = BeautifulSoup(html.text, 'html.parser')
    for tr in soup.select_one('div.cntBody table').select('tbody tr'):
        k = ' / '.join([tr.select('td')[-1].text, tr.select_one('td a').text.lstrip()])
        v = tr.select_one('td a')['onclick'].split(':')[-1]
        if '식단표' in k:    # 식단표면 skip
            continue
        menu.update({k: v})

print(*[f'[{i:2>}] {n}' for i, n in enumerate(menu)], sep='\n')
word = input("\n [!] 어떤 달의 식단을 분석할지 입력하세요 \n(2020년 9월이면 '2020년 9월', 2020년 방학이면 '2020년 여름방학'과 같이 입력) : ")
y, m = word.split(' ')
func = None
for i in menu:
    if y[:-1] in i and m in i:
        func = menu[i]
        break

file = ''
if func:
    try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('headless')
#         driver = webdriver.Chrome(r"C:\Users\user\Documents\chromedriver.exe", chrome_options=options)
        driver = webdriver.Chrome(r"C:\Users\user\Documents\chromedriver.exe")
        driver.get('http://dsmhs.djsch.kr/boardCnts/list.do?type=default&page=1&m=020503&s=dsmhs&boardID=54797')
        time.sleep(2)
        driver.execute_script(func)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
#         print('http://dsmhs.djsch.kr' + soup.select_one('article.board-text div.fieldBox dd a')['href'])
#         print('http://dsmhs.djsch.kr' + soup.select_one('article.board-text div.fieldBox dd a.previewConvert')['href'])
        file = 'http://dsmhs.djsch.kr' + soup.select_one('article.board-text div.fieldBox dd a')['href']
    finally:
        driver.close()

import pandas as pd

print(file)
xl=pd.ExcelFile(file)
meal_li = []
for meal in ['조식', '중식', '석식']:
    li = []
    for i in range(len(xl.parse(meal))//38):
        # df = pd.DataFrame(xl.parse(meal)[i*38:(i+1)*38+1], columns=[f"r{i}" for i in range(12)])
        df = xl.parse(meal)[i*39:(i+1)*39+1]
        # del df['r7']
        del df['Unnamed: 8']
        li.append(df)
    meal_li.append(li)
choice = input('[!] 무슨 작업을 하실 것인지 아래의 선택지 중 선택하세요'
               '\n(특정 날짜 식단 분석 -> 1, 특정 주간 식단 분석 -> 2, 월 전체 식단 분석 -> 3)\n(숫자를 입력하세요) : ')

choice = 2
if choice is 2:
    wek = int(input("원하는 주를 입력하세요 (첫번째 주면 '1'입력) : "))
    ran = int(input('선택지를 선택하세요\n(조식 분석 -> 1, 중식 분석 -> 2, 석식 분석 -> 3)\n(숫자를 입력하세요) : '))
# meal_li[0][0].T.tail(7)
    for i in range(ran-1, ran):1
        days = meal_li[i][wek-1].T.tail(7)
        print(days)
        print(days.T.head(3).tail(2).T)


# if choice is 1:
#     day = int(input("원하는 날짜를 입력하세요 (9일이면 '9'입력) : "))
#     ran = int(input("선택지를 선택하세요'
#                     '\n(조식, 중식, 석식 모두 분석 -> 0, 조식 분석 -> 1, 중식 분석 -> 2, 석식 분석 -> 3)\n(숫자를 입력하세요) : "))
#     s, l = ran-1, ran
#     if ran is 0:
#         s, l = 0, 3
#     for i in range(s, l):
#         for j in meal_li[i]
#             print(j.iloc[2])
