from django.db import models
from accounts.models import User


# class UploadImage(models.Model):
#     # title = models.CharField(max_length=255)
#     uploadedFile = models.FileField(upload_to="UploadImg/%Y/%m/%d")
#     create_date = models.DateTimeField(auto_now=True)
#     request_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Request(models.Model):
    # title = models.CharField(max_length=255)
    uploadedFile = models.FileField(upload_to="UploadImg/%Y/%m/%d")
    create_date = models.DateTimeField(auto_now=True)
    request_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    done = models.BooleanField(default=False)


class SearchedData(models.Model):
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    link = models.URLField(max_length=200)  #url이 얼마나 길어질지?
    img = models.FileField(upload_to="SearchedImg/%Y/%m/%d")




