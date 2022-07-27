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
        # input -> uploadedFile
        target_desc = face_comparison.img_encoding(str(uploadImg.uploadedFile))
        # Output -> SearchedData 타입, 저장하기.
        face_comparison.save_result(uploadImg, face_comparison.comparison(target_desc))
        return render(request, "mypageapp/mypage.html") # 요청완료 페이지

    return render(request, "searchapp/upload-file.html")