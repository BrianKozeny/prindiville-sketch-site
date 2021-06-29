from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages 
from .models import Video
from .forms import VideoForm

def index(request):
    firstvideo= Video.objects.all()
    videofile = []
    for video in firstvideo:
        videofile.append(video.file.url)


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context= {'videos': videofile,
              'form': form
              }


    return render(request, "dashboard/index.html", context)

def showvideo(request):

    firstvideo= Video.objects.all()
    videofile = []
    for video in firstvideo:
        videofile.append(video.file.url)


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Form submission successful')

    context= {'videos': videofile,
              'form': form
              }

    return render(request, 'dashboard/videos.html', context)

