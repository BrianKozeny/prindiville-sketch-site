from django import forms
from .models import Sketch, SketchFileUpload

class SketchForm(forms.ModelForm):
    class Meta:
        model = Sketch
        fields = ['title', 'description']
        

class ScriptUploadForm(forms.ModelForm):
    prefix = "script"
    class Meta:
        model = SketchFileUpload
        fields = ['file']
        labels = {
            "file": "Upload Script",
        }

class FootageUploadForm(forms.ModelForm):
    prefix = "footage"
    class Meta:
        model = SketchFileUpload
        fields = ['file']
        labels = {
            "file": "Upload Footage Clips",
        }
        
class FinalVideoUploadForm(forms.ModelForm):
    prefix = "final"
    class Meta:
        model = SketchFileUpload
        fields = ['file']
        labels = {
            "file": "Upload Final Video",
        }
