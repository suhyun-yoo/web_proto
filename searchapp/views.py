from . import models
from django.shortcuts import render, get_object_or_404, redirect
# from .models import UploadImage
import os
from django.conf import settings


def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["uploadedFile"]
        user = request.user
        # Saving the information in the database
        uploadImg = models.UploadImage(
            uploadedFile=uploadedFile,
            request_user=user
        )
        uploadImg.save()

    return render(request, "searchapp/upload-file.html")