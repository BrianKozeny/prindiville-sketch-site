from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Sketch, SketchFileUpload
from .forms import SketchForm, ScriptUploadForm, FootageUploadForm, FinalVideoUploadForm

# Test

from django.core.files.uploadedfile import SimpleUploadedFile

def index(request):

# ------ EXAMPLE ------
#
# shows a hard-coded example the demonstrates model relationships
# between Sketch and SketchFileUpload
#
#
#    sketch_val = Sketch.objects.create(title="Multiupload Test Sketch", description="test description")
#
#    fake_file_1 = SimpleUploadedFile(
#                    "brian_uploaded.txt",
#                    b"these are the file contents!" # note the b in front of the string [bytes]
#                ) 
#    fake_file_2 = SimpleUploadedFile(
#                    "joey_uploaded.txt",
#                    b"these are the file contents!" # note the b in front of the string [bytes]
#                ) 
#    fake_file_3 = SimpleUploadedFile(
#                    "chris_uploaded.txt",
#                    b"these are the file contents!" # note the b in front of the string [bytes]
#                ) 
#
#
#    sketch_val = Sketch.objects.filter(title='Multiupload Test Sketch').first()
#    fake_file_4 = SimpleUploadedFile(
#                    "chris_uploaded.txt",
#                    b"these are the file contents!" # note the b in front of the string [bytes]
#                ) 
#
#    file_upload_1 = SketchFileUpload.objects.create(file=fake_file_1, type="FOOTAGE", sketch=sketch_val)
#    file_upload_2 = SketchFileUpload.objects.create(file=fake_file_2, type="FOOTAGE", sketch=sketch_val)
#    file_upload_3 = SketchFileUpload.objects.create(file=fake_file_3, type="FOOTAGE", sketch=sketch_val)
#    file_upload_4 = SketchFileUpload.objects.create(file=fake_file_4, type="FINAL", sketch=sketch_val)


    firstsketch= Sketch.objects.all()

    return render(request, "dashboard/index.html",{ 'firstsketch': firstsketch })

def showsketch(request):

    if request.method == 'POST':
        form = SketchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        sketch_form = SketchForm()
        script_form = ScriptUploadForm()
        footage_form = FootageUploadForm()
        final_form = FinalVideoUploadForm()

        context = {
            "sketch_form": sketch_form,
            "script_form": script_form,
            "footage_form": footage_form,
            "final_form": final_form,
        }

    return render(request, 'dashboard/sketch.html', context)

