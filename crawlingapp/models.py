from django.db import models

# Create your models here.


class CrawringData(models.Model):
    link = models.URLField(max_length=200)  # url이 얼마나 길어질지?
    img = models.FileField(upload_to="CrawringImg/%Y/%m/%d")
