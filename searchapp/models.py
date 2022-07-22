from django.db import models
from accounts.models import User


class UploadImage(models.Model):
    # title = models.CharField(max_length=255)
    uploadedFile = models.FileField(upload_to="UploadImg/%Y/%m/%d")
    create_date = models.DateTimeField(auto_now=True)
    request_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


