from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Video
from .forms import VideoForm

def index(request):
    firstvideo= Video.objects.all()
    return render(request, "dashboard/index.html",{ 'firstvideo': firstvideo })

def showvideo(request):

    if request.method == 'POST':
        form= VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
            form = VideoForm()

    return render(request, 'dashboard/videos.html', { 'form': form })

