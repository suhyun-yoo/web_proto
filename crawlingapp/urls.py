from django.urls import path
from . import views

app_name = 'crawling'
urlpatterns = [
    path('', views.crawlingmain, name="main"),
    path('start/', views.crawlingstart, name="start"),
]
