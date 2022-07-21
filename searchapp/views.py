from . import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Document
import os
from django.conf import settings


def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

    return render(request, "searchapp/upload-file.html", context = {
        "files": documents
    })

def deleteFile(request, file_id):
    file = get_object_or_404(Document, pk=file_id)
    file_url = os.path.join(settings.MEDIA_ROOT, str(file.uploadedFile))
    print(file_url)
    os.remove(file_url)
    file.delete()
    return redirect('searchapp:uploadFile')
