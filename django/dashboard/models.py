from django.db import models

class Sketch(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class SketchFileUpload(models.Model):
    TYPE_CHOICES = [('FOOTAGE', 'Footage'), ('SCRIPT', 'Script'), ('FINAL', 'Final')]

    file = models.FileField(upload_to='videos/', null=True, blank=True)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, blank=False)
    sketch = models.ForeignKey(Sketch, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name

    """ 
    def delete(self, *args, **kwargs):
        self.file.storage.delete(self.SketchFileUpload.file)
        super().delete(*args, **kwargs)  
    """
