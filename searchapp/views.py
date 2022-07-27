from . import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Request, SearchedData
import os
from django.conf import settings
from . import face_comparison
from crawlingapp.models import CrawlingData


def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["uploadedFile"]
        user = request.user
        # Saving the information in the database
        uploadImg = models.Request(
            uploadedFile=uploadedFile,
            request_user=user
        )
        uploadImg.save()
        # search함수 부르기
        # result = img_encoding([uploadImg])
        # # img_encoding() 이라는 함수의 return type이 CrawlingData타입이어야
        # all_crawling_data = CrawlingData.objects.all().order_by("-id")
        # for res in result:
        #     searchedImg = models.SearchedData(
        #         request=uploadImg.id,
        #         img=uploadedFile,
        #         link=user
        #     )

        # input -> uploadedFile
        # Output -> SearchedData 타입, 저장하기.

    return render(request, "searchapp/upload-file.html")