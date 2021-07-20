from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    script = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name="Script")
    footage = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name="Footage")
    file = models.FileField(upload_to='videos/', null=True, blank=True,  verbose_name="Finished Sketch")

    def __str__(self):
        return self.title
