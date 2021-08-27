from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Sketch, SketchFileUpload
from .forms import SketchForm, ScriptUploadForm, FootageUploadForm, FinalVideoUploadForm

# Test

from django.core.files.uploadedfile import SimpleUploadedFile

def index(request):

    sketches_with_uploads = []

    sketches = Sketch.objects.all().prefetch_related('id__sketch_file_upload')

    for sketch in sketches:

        script_uploads = sketch.sketchfileupload_set.filter(type="SCRIPT").all()
        footage_uploads = sketch.sketchfileupload_set.filter(type="FOOTAGE").all()
        final_uploads = sketch.sketchfileupload_set.filter(type="FINAL").all()

        sketch_with_upload = {
            "title": sketch.title,
            "description": sketch.description,
            "script_uploads": script_uploads,
            "footage_uploads": footage_uploads,
            "final_uploads": final_uploads 
        }
        
        sketches_with_uploads.append(sketch_with_upload)

    return render(request, "dashboard/index.html",{ 'sketches': sketches_with_uploads })

def showsketch(request):

    # POST request
    if request.method == 'POST':

        sketch_form = SketchForm(request.POST, request.FILES)
        script_form = ScriptUploadForm(request.POST, request.FILES)
        footage_form = FootageUploadForm(request.POST, request.FILES)
        final_form = FinalVideoUploadForm(request.POST, request.FILES)

        forms_are_valid = (sketch_form.is_valid() and script_form.is_valid()
        and footage_form.is_valid() and final_form.is_valid())

        if forms_are_valid:
            # Save all forms correctly
            sketch_form_val = sketch_form.save()
            # Take id from sketch_form_val and set to each
            # script, footage, and final form if they exist

            script_data = script_form.cleaned_data
            footage_data = footage_form.cleaned_data
            final_data = final_form.cleaned_data


            if script_data['file']:
                SketchFileUpload.objects.create(
                    file=script_data['file'],
                    type="SCRIPT",
                    sketch=sketch_form_val
                )

            if footage_data['file']:
                SketchFileUpload.objects.create(
                    file=footage_data['file'],
                    type="FOOTAGE",
                    sketch=sketch_form_val
                )

            if final_data['file']:
                SketchFileUpload.objects.create(
                    file=final_data['file'],
                    type="FINAL",
                    sketch=sketch_form_val
                )

            return redirect('index')

    # GET request
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

