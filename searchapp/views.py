from . import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Request
import os
from django.conf import settings


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
        # Output -> SearchedData 타입, 저장하기.

    return render(request, "searchapp/upload-file.html")