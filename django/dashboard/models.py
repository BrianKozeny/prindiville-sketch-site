from django.db import models

class Sketch(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class SketchFileUpload(models.Model):
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    type = models.CharField(max_length=100)
    sketch = models.ForeignKey(Sketch, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
