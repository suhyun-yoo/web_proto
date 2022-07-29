import os
from os.path import getsize
from urllib.request import urlopen
from urllib.request import urlretrieve
# from urllib.parse import quote_plus # 아스키 코드로 변환시켜준다.
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
from .models import CrawlingData
import requests
from urllib import request

## chrome webdriver option ##
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(r'chromedriver', options=options)


def get_url(board, start_date, end_date):  # 게시판 파싱한거 input
    ## 크롤링 시작 ##
    n = 1  # 글 한개마다 +1
    if type(start_date) == str:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    for i in board:
        # w_date = i.select_one('td:nth-of-type(4)')['title']  # 작성일
        # w_date = datetime.strptime(w_date[:10], '%Y-%m-%d')
        #
        # if start_date > w_date or w_date > end_date:  # 지정한 기간 밖일 때
        #     break
        # else:
        num = i['data-no']  # 글넘버
        link = 'https://gall.dcinside.com' + i.a['href']
        title = i.a.text

        img_exist = i.a.em  # icon_img icon_pic 포함할 경우 사진 있음
        if 'icon_img icon_pic' in str(img_exist):  # 사진/동영상 있는 경우
            # image_download(link)
            print('게시글 번호 : ' + num)  # 글넘버
            # print('작성일 : ' + str(w_date))  # 작성일
            print(f'title {n} --> ' + title)  # 게시글 제목
            print('게시글 링크 --> ' + link)  # 각 게시글 링크
            driver.get(link)  # 사진있는 게시글 링크 불러옴
            time.sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            write_area = soup.select('.write_div img')

            # 이미지 링크 출력
            for k in write_area:
                img_link = k['src']
                no = img_link.split('=')[-1]
                img_click = 'https://image.dcinside.com/viewimagePop.php?no=' + no  # 실제 사진 링크
                img_src = "https://image.dcinside.com/viewimage.php?id=&no=" +no
                driver.implicitly_wait(2)
                # print('이미지 링크 --> ' + img_click)  # img_click link
                # jpg로 save
                img_name = 'media/'+num+'.jpg'

                # r = requests.get(img_src)
                # file = open(img_name, 'wb')
                # file.write(r.content)
                # file.close()
                urlretrieve(img_click, img_name)
                crawlingimg = CrawlingData(
                    link=link,
                    img=img_name,
                )
                crawlingimg.save()
            driver.back()  # 뒤로가기

        n += 1
    driver.quit()


## 원하는 갤러리, 페이지 긁어오기 ##
# 크롤링 할 갤러리, 페이지 지정
def show_board(boardname, pagenum, start_date, end_date):
    print("in!!!!!!")
    # end_date = input("날짜입력 : ")
    for i in range(1):
        baseUrl = 'https://gall.dcinside.com/board/lists/?id={}&page={}'.format(boardname, pagenum+i)

        driver.get(baseUrl)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        board = soup.select('.ub-content.us-post')
        get_url(board, start_date, end_date)  # 크롤링 함수 호출


if __name__ == "__main__":
    # show_board("programming", 1)
    # show_board("strangelawyer", 1)
    show_board("brahms", 1, start_date=datetime.now(), end_date="2022-07-25") # 브람스를 좋아하세요?

    # 이후에는 게시판목록 리스트를 board_list에 담고
    # for board in board_list:
    #     show_board(board, 1)