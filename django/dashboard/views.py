from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from django.db import transaction
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
            "id": sketch.pk,
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
        print("FORMS ARE VALID: ", forms_are_valid)

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
        else:
            print("Form is not valid")

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

def edit_sketch(request, id):

    sketch = Sketch.objects.get(id=id)
    script_uploads = SketchFileUpload.objects.filter(sketch_id = id, type="SCRIPT")
    footage_uploads = SketchFileUpload.objects.filter(sketch_id = id, type="FOOTAGE")
    final_uploads = SketchFileUpload.objects.filter(sketch_id = id, type="FINAL")

    if request.method == 'POST':
        filled_form = SketchForm(request.POST, instance = sketch)
        print("REQUEST POST: ", request.POST)
        print("REQUEST FILES: ", request.FILES)

        # Check form and deleted files
        for key, val in request.POST.items():
            if not val:
                continue 

            if key == "title":
                sketch.title = val
                print("Title", val)

            elif key == "description":
                sketch.description = val 
                print("Description", val)


        # Check file uploads (STILL NEED TO DO)
        for key, val in request.FILES.items():
            if key == "new-script-file":
                SketchFileUpload.objects.create(
                    file=val,
                    type="SCRIPT",
                    sketch=sketch
                )
                print("New Script File:", val)

            elif key == "new-footage-file":
                SketchFileUpload.objects.create(
                    file=val,
                    type="FOOTAGE",
                    sketch=sketch
                )
                print("New Footage File:", val)

            elif key == "new-final-file":
                with transaction.atomic():
                    final_upload = SketchFileUpload.objects.create(
                        type="FINAL",
                        sketch=sketch
                    )
                    final_upload.file.save(val.name, val)
            

        return redirect('index')
    else:
        
        sketch_form = SketchForm(instance = sketch)

        new_script_form = ScriptUploadForm(prefix="new-script")
        new_footage_form = FootageUploadForm(prefix="new-footage")
        new_final_form = FinalVideoUploadForm(prefix="new-final")

        context = {
            "sketch_form": sketch_form,
            "new_script_form": new_script_form,
            "new_footage_form": new_footage_form,
            "new_final_form": new_final_form,
            "script_uploads": script_uploads,
            "footage_uploads": footage_uploads,
            "final_uploads":  final_uploads,
        }

        return render(request, 'dashboard/edit_sketch.html', context)

def delete_sketch(request, id):
    sketch = Sketch.objects.get(id=id)
    uploads = SketchFileUpload.objects.filter(sketch_id = id)
    uploads.delete()
    sketch.delete()

    return redirect('index')


def delete_upload(request, sketch_id, upload_id):
    upload = SketchFileUpload.objects.get(id = upload_id)
    upload.delete()
    return redirect('/edit/' + str(sketch_id))
