import time

from . import models
from django.shortcuts import render, get_object_or_404, redirect
from . import face_comparison


def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["uploadedFile"]
        user = request.user
        # Saving the information in the database
        # print(uploadedFile)
        # print(type(uploadedFile))
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
        return redirect("mypage:mypage") # 요청완료 페이지

    return render(request, "searchapp/upload-file.html")