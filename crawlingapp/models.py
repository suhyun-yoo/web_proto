from django.db import models
# Create your models here.


class CrawlingData(models.Model):
    link = models.URLField(max_length=200)  # url이 얼마나 길어질지?
    img = models.FileField(upload_to="CrawlingImg", max_length=200)
    batch_date = models.DateField(auto_now_add=True)
