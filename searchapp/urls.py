from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

app_name = "searchapp"

urlpatterns = [
    path("", views.uploadFile, name = "uploadFile"),
    path('deleteFile/<int:file_id>/', views.deleteFile, name='delete'),

]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )