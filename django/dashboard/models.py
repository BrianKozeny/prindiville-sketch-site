from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    file = models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.title
