from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
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

            if "clear" in key:
                id = key[0]
                file_upload = SketchFileUpload.objects.get(id=id)
                print("Deleting file:", file_upload.file)
                # some delete method for SketchFileUpload with id
                # as well as os file deletion (be careful!)

            elif key == "title":
                sketch.title = val
                print("Title", val)

            elif key == "description":
                sketch.description = val 
                print("Description", val)


        # Check file uploads
        for key, val in request.FILES.items():
            if key == "new-script-file":
                print("New Script File:", val)

            elif key == "new-footage-file":
                print("New Footage File:", val)

            elif key == "new-final-file":
                print("New Final File:", val)
            

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
    script = SketchFileUpload.objects.filter(sketch_id = id, type="SCRIPT")
    footage = SketchFileUpload.objects.filter(sketch_id = id, type="FOOTAGE")
    final = SketchFileUpload.objects.filter(sketch_id = id, type="FINAL")
    sketch.delete()
    script.delete()
    footage.delete()
    final.delete()

    return redirect('index')

def delete_script(request, sketch_id, script_id):
    sketch = Sketch.objects.get(id=sketch_id)
    script = SketchFileUpload.objects.filter(id = script_id, type="SCRIPT")
    sketch_form = SketchForm(instance = sketch)
    new_script_form = ScriptUploadForm(prefix="new-script")
    new_footage_form = FootageUploadForm(prefix="new-footage")
    new_final_form = FinalVideoUploadForm(prefix="new-final")
    script_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="SCRIPT")
    footage_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="FOOTAGE")
    final_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="FINAL")

    context = {
        "sketch_form": sketch_form,
        "new_script_form": new_script_form,
        "new_footage_form": new_footage_form,
        "new_final_form": new_final_form,
        "script_uploads": script_uploads,
        "footage_uploads": footage_uploads,
        "final_uploads":  final_uploads,
    }

    script.delete()

    return render(request, 'dashboard/edit_sketch.html', context)

def delete_footage(request, sketch_id, footage_id):
    sketch = Sketch.objects.get(id=sketch_id)
    footage = SketchFileUpload.objects.filter(id = footage_id, type="FOOTAGE")
    sketch_form = SketchForm(instance = sketch)
    new_script_form = ScriptUploadForm(prefix="new-script")
    new_footage_form = FootageUploadForm(prefix="new-footage")
    new_final_form = FinalVideoUploadForm(prefix="new-final")
    script_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="SCRIPT")
    footage_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="FOOTAGE")
    final_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="FINAL")

    context = {
        "sketch_form": sketch_form,
        "new_script_form": new_script_form,
        "new_footage_form": new_footage_form,
        "new_final_form": new_final_form,
        "script_uploads": script_uploads,
        "footage_uploads": footage_uploads,
        "final_uploads":  final_uploads,
    }

    footage.delete()

    return render(request, 'dashboard/edit_sketch.html', context)

def delete_final(request, sketch_id, final_id):
    sketch = Sketch.objects.get(id=sketch_id)
    final = SketchFileUpload.objects.filter(id = final_id, type="FINAL")
    sketch_form = SketchForm(instance = sketch)
    new_script_form = ScriptUploadForm(prefix="new-script")
    new_footage_form = FootageUploadForm(prefix="new-footage")
    new_final_form = FinalVideoUploadForm(prefix="new-final")
    script_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="SCRIPT")
    footage_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="FOOTAGE")
    final_uploads = SketchFileUpload.objects.filter(sketch_id = sketch_id, type="FINAL")

    context = {
        "sketch_form": sketch_form,
        "new_script_form": new_script_form,
        "new_footage_form": new_footage_form,
        "new_final_form": new_final_form,
        "script_uploads": script_uploads,
        "footage_uploads": footage_uploads,
        "final_uploads":  final_uploads,
    }

    final.delete()

    return render(request, 'dashboard/edit_sketch.html', context)
