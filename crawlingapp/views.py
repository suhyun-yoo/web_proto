from django.shortcuts import render, redirect
from crawlingapp import crawling_selenium
from datetime import datetime
from crawlingapp import crawling
# Create your views here.


def crawlingmain(request):
    return render(request, 'crawlingapp/crawling_test.html')


def crawlingstart(request):
    # crawling_selenium.show_board("brahms", 1, start_date=datetime.now(), end_date="2022-07-25") # 브람스를 좋아하세요?
    crawling.img_crawling("brahms", 1)
    return redirect('/main/')